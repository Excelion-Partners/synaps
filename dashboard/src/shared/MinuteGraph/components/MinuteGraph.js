import React from 'react'
import PropTypes from 'prop-types'
import './MinuteGraph.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class MinuteGraph extends React.Component {
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
				type: 'spline',
				animation: ReactHighcharts.Highcharts.svg
				// options3d: {
				//     enabled: true,
				//     alpha: 5,
				//     beta: 5,
				//     depth: 50,
				//     viewDistance: 40
				// }
			},
			title: {
				text: 'Sessions per Minute'
			},
			// subtitle: {
			//     text: document.ontouchstart === undefined ?
			//         'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
			// },
			xAxis: {
				gridLineColor: 'transparent',
				//  type: 'datetime',
				// dateTimeLabelFormats: { // don't display the dummy year
				//     month: '%e. %b',
				//     year: '%b'
				// },
				title: {
					text: 'Date'
				},
				labels: {
					style: {
						'font-size': '15px'
					}
				}
			},
			yAxis: {
				gridLineColor: 'transparent',
				labels: {
					style: {
						'font-size': '15px'
					}
				},
				title: {
					text: 'Views'
				}
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

		return (
			<ReactHighcharts config={config} />
		)
	}
}

MinuteGraph.propTypes = {
	data: PropTypes.array.isRequired
}

export default MinuteGraph
