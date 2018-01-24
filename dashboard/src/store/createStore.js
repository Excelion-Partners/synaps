import { applyMiddleware, compose, createStore } from 'redux'
import thunk from 'redux-thunk'
import createLogger from 'redux-logger'
import { persistStore, autoRehydrate } from 'redux-persist'
import { apiMiddleware } from 'redux-api-middleware'
import { asyncSessionStorage } from 'redux-persist/storages'
import { browserHistory } from 'react-router'
import makeRootReducer from './reducers'
import { updateLocation } from './location'

export default (initialState = {}) => {
	return new Promise((resolve, reject) => {
		try {
			// ======================================================
			// Middleware Configuration
			// ======================================================
			const logger = createLogger()
			const middleware = [apiMiddleware, thunk, logger]

			// ======================================================
			// Store Enhancers
			// ======================================================
			const enhancers = [autoRehydrate()]

			let composeEnhancers = compose

			if (__DEV__) {
				const composeWithDevToolsExtension = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
				if (typeof composeWithDevToolsExtension === 'function') {
					composeEnhancers = composeWithDevToolsExtension
				}
			}

			// ======================================================
			// Store Instantiation and HMR Setup
			// ======================================================
			const store = createStore(
				makeRootReducer(),
				initialState,
				composeEnhancers(
					applyMiddleware(...middleware),
					...enhancers
				)
			)

			store.asyncReducers = {}

			// To unsubscribe, invoke `store.unsubscribeHistory()` anytime
			store.unsubscribeHistory = browserHistory.listen(updateLocation(store))

			if (module.hot) {
				module.hot.accept('./reducers', () => {
					const reducers = require('./reducers').default
					store.replaceReducer(reducers(store.asyncReducers))
				})
			}

			persistStore(store, { storage: asyncSessionStorage }, () => { resolve(store) })
		} catch (e) {
			reject(e)
		}
	})
}
