import React from 'react'
import PropTypes from 'prop-types'
import './CoreLayout.scss'
import '../../../styles/core.scss'
import '../../../styles/luna.scss'
import '../../../styles/fontawesome/css/font-awesome.scss'

export const CoreLayout = (props) => {
	const { children } = props

	return (
		<div className='wrapper'>
			{children}
		</div>
	)
}

CoreLayout.propTypes = {
	children: PropTypes.element.isRequired
}

export default CoreLayout
