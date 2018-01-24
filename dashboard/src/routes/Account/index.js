import AccountView from './components/AccountView'
import LoginRoute from './routes/Login'

// Sync route definition
export default (store) => ({
	path: 'account',
	component: AccountView,
	childRoutes: [
		LoginRoute(store)
	]
})
