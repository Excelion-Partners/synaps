import React from 'react'
import PropTypes from 'prop-types'
import './GenderPie.scss'
import ReactHighcharts from 'react-highcharts'
import Theme from '../../../styles/highcharts/themes/DarkUnica'

export class GenderPie extends React.Component {
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
				type: 'pie'
				// options3d: {
				//     enabled: true,
				//     alpha: 45,
				//     beta: 0
				// }
			},
			title: {
				text: '24 hr Gender'
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

		return (
			<ReactHighcharts config={config} style={style} />
		)
	}
}

GenderPie.propTypes = {
	data: PropTypes.array.isRequired
}

export default GenderPie
