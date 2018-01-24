import React from 'react'
import PropTypes from 'prop-types'
import './LineChart.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class LineChart extends React.Component {
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
				type: this.props.lineType,
				height: 300,
				animation: ReactHighcharts.Highcharts.svg
			},
			title: {
				text: this.props.title
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
			legend: {
				enabled: false
			},
			plotOptions: {
				line: {
					animation: false
				},
				area: {
					animation: false,
					fillColor: {
						linearGradient: {
							x1: 0,
							y1: 0,
							x2: 0,
							y2: 1
						},
						stops: [
							[0, ReactHighcharts.Highcharts.getOptions().colors[0]],
							[
								1,
								ReactHighcharts.Highcharts.Color(ReactHighcharts.Highcharts.getOptions().colors[0])
								.setOpacity(0).get('rgba')
							]
						]
					},
					marker: {
						radius: 2
					},
					lineWidth: 1,
					states: {
						hover: {
							lineWidth: 1
						}
					},
					threshold: null
				}
			},

			series: [{
				animation: false,
				data: this.props.data
			}]
		}

		return (<ReactHighcharts config={config} />)
	}
}

LineChart.propTypes = {
	title: PropTypes.string.isRequired,
	lineType: PropTypes.string.isRequired,
	xAxisTitle: PropTypes.string.isRequired,
	yAxisTitle: PropTypes.string.isRequired,
	data: PropTypes.array.isRequired,
	categories: PropTypes.array.isRequired
}

export default LineChart
