import React from 'react'
import PropTypes from 'prop-types'
import './AccountView.scss'

export const AccountView = (props) => (
	<div className='account-content'>
		{props.children}
	</div>
)

AccountView.propTypes = {
	children: PropTypes.element.isRequired
}

export default AccountView
