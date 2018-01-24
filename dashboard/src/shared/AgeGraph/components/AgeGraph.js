import React from 'react'
import PropTypes from 'prop-types'
import './AgeGraph.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class AgeGraph extends React.Component {
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
				// options3d: {
				//     enabled: true,
				//     alpha: 5,
				//     beta: 5,
				//     depth: 50,
				//     viewDistance: 40
				// }
			},
			title: {
				text: '24 hr Age'
			},
			xAxis: {
				gridLineColor: 'transparent',
				title: {
					text: 'Age'
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
				type: 'column',
				data: this.props.data
			}]
		}

		return (
			<ReactHighcharts config={config} style={style} />
		)
	}
}

AgeGraph.propTypes = {
	categories: PropTypes.array.isRequired,
	data: PropTypes.array.isRequired
}

export default AgeGraph
