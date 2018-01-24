import CoreLayout from '../layouts/CoreLayout'
import DashboardRoute from './Dashboard'

export const createRoutes = (store) => ({
	path: '/',
	childRoutes: [
		{
			component: CoreLayout,
			indexRoute: DashboardRoute(store),
			childRoutes: [
			]
		}
	]
})

export default createRoutes
