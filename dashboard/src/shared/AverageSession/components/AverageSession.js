import React from 'react'
import PropTypes from 'prop-types'
import './AverageSession.scss'

export const AverageSession = (props) => {
	const { sessionTime } = props

	var colorFont = {
		color: '#fff',
		fontSize: '60px'
	}

	return (
		<div>
			<h4>AVG SESSION:</h4>
			<div id='avgTime' style={colorFont}>{sessionTime}</div>
		</div>
	)
}

AverageSession.propTypes = {
	sessionTime: PropTypes.string.isRequired
}

export default AverageSession
