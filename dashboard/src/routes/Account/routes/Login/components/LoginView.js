import React from 'react'
import PropTypes from 'prop-types'
import LoginForm from './LoginForm'
import './LoginView.scss'

export const LoginView = (props) => {
	const { onSubmit } = props

	return (
		<div className='center-login'>
			<LoginForm onSubmit={onSubmit} />
		</div>
	)
}

LoginView.propTypes = {
	onSubmit: PropTypes.func.isRequired
}

export default LoginView
