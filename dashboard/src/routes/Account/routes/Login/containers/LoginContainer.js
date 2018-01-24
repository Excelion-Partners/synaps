import { connect } from 'react-redux'
import { browserHistory } from 'react-router'
import LoginView from '../components/LoginView'

const mapDispatchToProps = {
	onSubmit: () => {
		sessionStorage.setItem('access_token', 'test_key')
		browserHistory.push('/')
	}
}

const mapStateToProps = (state) => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(LoginView)
