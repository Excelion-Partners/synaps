import React from 'react'
import './ActiveSessions.scss'
import UnknownImage from '../assets/unknown.png'

export const ActiveSessions = () => {
	var label = {
		color: '#f2f2f2',
		fontSize: '22px',
		textAlign: 'center'
	}

	var opacityDot2 = {
		opacity: '.2'
	}

	var opacity1 = {
		opacity: '1'
	}

	return (
		<div>
			<div style={label}>ACTIVE SESSIONS:</div>
			<div id='active-sessions' />
			<div id='no-sessions'>
				<div className='session-info' style={opacityDot2}>
					<div>
						<img src={UnknownImage} className='avatar' style={opacity1} />

					</div>
				</div>
				<div className='session-info' style={opacityDot2}>
					<div>
						<img src={UnknownImage} className='avatar' style={opacity1} />

					</div>
				</div>
				<div className='session-info' style={opacityDot2}>
					<div>
						<img src={UnknownImage} className='avatar' style={opacity1} />

					</div>
				</div>
				<div className='session-info' style={opacityDot2}>
					<div>
						<img src={UnknownImage} className='avatar' style={opacity1} />

					</div>
				</div>
			</div>
		</div>
	)
}

export default ActiveSessions
