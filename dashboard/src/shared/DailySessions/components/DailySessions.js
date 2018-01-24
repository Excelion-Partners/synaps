import React from 'react'
import './DailySessions.scss'

export const DailySessions = () => {
	var colorFont = {
		color: '#fff',
		fontSize: '60px'
	}

	return (
		<div>
			<h4>DAILY SESSIONS:</h4>
			<div id='total_sessions' style={colorFont} />
		</div>
	)
}

export default DailySessions
