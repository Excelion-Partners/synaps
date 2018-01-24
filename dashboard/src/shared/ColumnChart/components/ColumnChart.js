import React from 'react'
import PropTypes from 'prop-types'
import './ColumnChart.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class ColumnChart extends React.Component {
	constructor(props) {
		super(props)

		this._setTheme = this._setTheme.bind(this)
	}

	_setTheme() {
		ReactHighcharts.Highcharts.theme = Theme
		ReactHighcharts.Highcharts.setOptions(ReactHighcharts.Highcharts.theme)
	}

	componentWillMount() {
		this._setTheme()
	}

	render() {
		var config = {
			chart: {
				type: 'column',
				height: 300
			},
			title: {
				text: this.props.title
			},
			legend: {
				enabled: false
			},
			xAxis: {
				gridLineColor: 'transparent',
				title: {
					text: this.props.xAxisTitle
				},
				labels: {
					style: {
						'font-size': '15px'
					}
				},
				categories: this.props.categories
			},
			yAxis: {
				gridLineColor: 'transparent',
				labels: {
					style: {
						'font-size': '15px'
					}
				},
				title: {
					text: this.props.yAxisTitle
				},
				min: 0
			},
			plotOptions: {
				column: {
					pointPadding: 0.2,
					borderWidth: 0
				}
			},
			series: this.props.series
		}

		return (<ReactHighcharts config={config} />)
	}
}

ColumnChart.propTypes = {
	title: PropTypes.string.isRequired,
	xAxisTitle: PropTypes.string.isRequired,
	yAxisTitle: PropTypes.string.isRequired,
	categories: PropTypes.array.isRequired,
	series: PropTypes.array.isRequired
}

export default ColumnChart
