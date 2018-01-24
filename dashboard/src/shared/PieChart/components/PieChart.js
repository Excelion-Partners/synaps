import React from 'react'
import PropTypes from 'prop-types'
import './PieChart.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class PieChart extends React.Component {
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
		var style = {
			width: '100%',
			height: '400px'
		}

		var config = {
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false,
				type: 'pie',
				height: 300
			},
			title: {
				text: this.props.title
			},
			tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
			},
			plotOptions: {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					depth: 35,
					dataLabels: {
						enabled: true,
						format: '<b>{point.name}</b>: {point.percentage:.1f} %',
						style: {
							color: (ReactHighcharts.Highcharts.theme && ReactHighcharts.Highcharts.theme.contrastTextColor) ||
							'black'
						}
					}
				}
			},
			series: this.props.data
		}

		return (<
			ReactHighcharts config={
				config
			}
			style={
				style
			}
		/>
		)
	}
}

PieChart.propTypes = {
	title: PropTypes.string.isRequired,
	data: PropTypes.array.isRequired
}

export default PieChart
