import React from 'react'
import ReactDOM from 'react-dom'
// import { reducer as formReducer } from 'redux-form'
import createStore from './store/createStore'
import AppContainer from './shared/App/containers/AppContainer'
import { browserHistory } from 'react-router'
// import { injectReducer } from './store/reducers'

async function init() {
	// ========================================================
	// Store Instantiation
	// ========================================================
	const initialState = window.___INITIAL_STATE__
	const store = await createStore(initialState)

	// Inject redux-form
	// store.asyncReducers['form'] = formReducer

	// ========================================================
	// Render Setup
	// ========================================================
	const MOUNT_NODE = document.getElementById('root')

	let render = () => {
		const routes = require('./routes/index').default(store)

		ReactDOM.render(
			<AppContainer store={store} routes={routes} />,
			MOUNT_NODE
		)
	}

	browserHistory.listen(location => {
		const path = (/#!(\/.*)$/.exec(location.hash) || [])[1]
		if (path) {
			history.replace(path)
		}
	})

	// This code is excluded from production bundle
	if (__DEV__) {
		if (module.hot) {
			// Development render functions
			const renderApp = render
			const renderError = (error) => {
				const RedBox = require('redbox-react').default

				ReactDOM.render(<RedBox error={error} />, MOUNT_NODE)
			}

			// Wrap render in try/catch
			render = () => {
				try {
					renderApp()
				} catch (error) {
					console.error(error)
					renderError(error)
				}
			}

			// Setup hot module replacement
			module.hot.accept('./routes/index', () =>
				setImmediate(() => {
					ReactDOM.unmountComponentAtNode(MOUNT_NODE)
					render()
				})
			)
		}
	}

	// ========================================================
	// Go!
	// ========================================================
	render()
}

init()
