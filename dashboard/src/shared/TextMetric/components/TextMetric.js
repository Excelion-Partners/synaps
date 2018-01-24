import React from 'react'
import PropTypes from 'prop-types'
import './TextMetric.scss'

export class TextMetric extends React.Component {
	render() {
		return (
			<div className='panel panel-filled'>
				<div className='panel-body'>
					<h2 className='m-b-none'>
						{this.props.data}
						<span className='slight'><i className='fa fa-play fa-rotate-270 text-warning' /> +{this.props.trend}%</span>

					</h2>
					<div className='small'>{this.props.title}</div>
				</div>
			</div>
		)
	}
}

TextMetric.propTypes = {
	title: PropTypes.string.isRequired,
	data: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
	trend: PropTypes.number.isRequired
}

export default TextMetric
