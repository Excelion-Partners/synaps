import React from 'react'
import PropTypes from 'prop-types'
import { Field, reduxForm } from 'redux-form'

export const LoginForm = (props) => {
	const { handleSubmit } = props

	return (
		<div>
			<form
				onSubmit={handleSubmit}
				className='input-group login-form'>
				<h2 className='form-signin-heading'>Please login</h2>
				<Field name='username' component='input' type='text' className='form-control' placeholder='Username' required />
				<Field name='password' component='input' type='password' className='form-control' placeholder='Password'
					required />
				<button className='btn btn-lg btn-primary btn-block' type='submit'>Login</button>
			</form>
		</div>
	)
}

LoginForm.propTypes = {
	handleSubmit: PropTypes.func.isRequired
}

export default reduxForm({
	form: 'login'
})(LoginForm)
