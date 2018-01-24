import React from 'react'
import axios from 'axios'
import Promise from 'bluebird'
import './DashboardView.scss'
import Header from '../../../shared/Header'
import LeftNav from '../../../shared/LeftNav'
import LiveFeed from '../../../shared/LiveFeed'
import ColumnChart from '../../../shared/ColumnChart'
import PieChart from '../../../shared/PieChart'
import TextMetric from '../../../shared/TextMetric'

export default class DashboardView extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			totalTraffic: 0,
			totalTrafficTrend: 0,
			totalOpportunities: 0,
			totalOpportunitiesTrend: 0,
			avgDailyTraffic: 0,
			avgDailyTrafficTrend: 0,
			avgDailyOpportunities: 0,
			avgDailyOpportunitiesTrend: 0,
			genderRatio: '0/0',
			genderRatioTrend: 0,
			avgViewDuration: 0,
			avgViewDurationTrend: 0,
			trafficGenderPieData: [],
			opportunitiesGenderPieData: [],
			trafficAgePieData: [],
			opportunitiesAgePieData: [],
			traphicByHoursChartCategories: [],
			traphicByHoursChartSeries: []
		}

		this._generatePieDataArray = this._generatePieDataArray.bind(this)
		this._loadData = this._loadData.bind(this)
	}

	_generatePieDataArray(arr) {
		var resultArray = []
		arr.forEach(function(element) {
			resultArray.push(
				{
					name: element.label,
					y: element.value
				}
			)
		})

		return resultArray
	}

	_loadData() {
		Promise.all([
			axios({
				method: 'get',
				url: 'https://urbjjaudbh.execute-api.us-east-1.amazonaws.com/dev/session/getLastDay'
			}),
			axios({
				method: 'get',
				url: 'https://urbjjaudbh.execute-api.us-east-1.amazonaws.com/dev/session/getSevenDays'
			})
		]).then((result) => {
			var dataOne = result[0].data
			var dataSeven = result[1].data
			console.log(dataOne)
			console.log(dataSeven)

			var trafficGenderPieData = [{
				animation: false,
				name: 'Gender',
				colorByPoint: true,
				data: this._generatePieDataArray(dataOne.sessionsByGender)
			}]

			var opportunitiesGenderPieData = [{
				animation: false,
				name: 'Gender',
				colorByPoint: true,
				data: this._generatePieDataArray(dataOne.opportunitiesByGender)
			}]

			var trafficAgePieData = [{
				animation: false,
				name: 'Gender',
				colorByPoint: true,
				data: this._generatePieDataArray(dataOne.sessionsByAgeGroup)
			}]

			var opportunitiesAgePieData = [{
				animation: false,
				name: 'Gender',
				colorByPoint: true,
				data: this._generatePieDataArray(dataOne.opportunitiesByAgeGroup)
			}]

			var traphicByHoursChartCategories = []

			var traphicByHoursChartData = []

			dataOne.sessionsByHourInterval.forEach(function(element) {
				traphicByHoursChartCategories.push(element.label)
				traphicByHoursChartData.push(element.value)
			})

			var traphicByHoursChartSeries = [
				{
					name: 'Views',
					data: traphicByHoursChartData
				}
			]

			var maleCount = 0
			var femaleCount = 0

			dataOne.sessionsByGender.forEach(function(element) {
				if (element.key === 'male') {
					maleCount = element.value
				} else {
					femaleCount = element.value
				}
			})

			this.setState({
				totalTraffic: dataOne.totalSessions,
				totalTrafficTrend: dataOne.totalSessionsTrend,
				totalOpportunities: dataOne.totalOpportunities,
				totalOpportunitiesTrend: dataOne.totalOpportunitiesTrend,
				avgDailyTraffic: Math.ceil(dataSeven.avgDailySessions),
				avgDailyTrafficTrend: dataSeven.avgDailySessionsTrend,
				avgDailyOpportunities: Math.ceil(dataSeven.avgDailyOpportunities),
				avgDailyOpportunitiesTrend: dataSeven.avgDailyOpportunitiesTrend,
				genderRatio: maleCount + '/' + femaleCount,
				genderRatioTrend: dataOne.totalSessionsTrend,
				avgViewDuration: dataOne.avgViewDuration.toFixed(1),
				avgViewDurationTrend: dataOne.avgViewDurationTrend,
				trafficGenderPieData: trafficGenderPieData,
				opportunitiesGenderPieData: opportunitiesGenderPieData,
				trafficAgePieData: trafficAgePieData,
				opportunitiesAgePieData: opportunitiesAgePieData,
				traphicByHoursChartCategories: traphicByHoursChartCategories,
				traphicByHoursChartSeries: traphicByHoursChartSeries
			})
		})
	}

	componentDidMount() {
		this._loadData()

		var self = this
		setInterval(function() {
			self._loadData()
		}, 60000)
	}

	render() {
		var topPadding2 = {
			paddingTop: '2px'
		}

		var clear = {
			'clear': 'both'
		}

		return (
			<div>
				<Header />
				<LeftNav />
				<section className='content'>
					<div className='container-fluid'>

						<div className='row'>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric
									title='Total Traffic'
									data={this.state.totalTraffic}
									trend={this.state.totalTrafficTrend} />
							</div>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric
									title='Total Opportunities'
									data={this.state.totalOpportunities}
									trend={this.state.totalOpportunitiesTrend} />
							</div>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric title='Average Daily Traffic'
									data={this.state.avgDailyTraffic}
									trend={this.state.avgDailyTrafficTrend} />
							</div>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric
									title='Avg Daily Opportunities'
									data={this.state.avgDailyOpportunities}
									trend={this.state.avgDailyOpportunitiesTrend} />
							</div>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric title='Gender Ratio (M/F)'
									data={this.state.genderRatio}
									trend={this.state.genderRatioTrend} />
							</div>
							<div className='col-lg-2 col-xs-6'>
								<TextMetric title='Average View Duration'
									data={this.state.avgViewDuration}
									trend={this.state.avgViewDurationTrend} />
							</div>
						</div>

						<div className='row'>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<PieChart title='Traffic By Gender' data={this.state.trafficGenderPieData} />
									</div>
								</div>
							</div>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<div style={topPadding2} id='video_feed'>
											<LiveFeed />
										</div>
									</div>
									{ /* <div className='col-md-6 center' style={topPadding10} id='avatars'>
										<ActiveSessions />
									</div> */ }
									<div style={clear} />
								</div>
							</div>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<PieChart title='Traffic By Age' data={this.state.trafficAgePieData} />
									</div>
								</div>
							</div>
						</div>
						<div className='row'>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<PieChart title='Opportunities By Gender' data={this.state.opportunitiesGenderPieData} />
									</div>
								</div>
							</div>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<ColumnChart
											title='Daily Traffic Intervals'
											xAxisTitle='Time'
											yAxisTitle='Views'
											categories={this.state.traphicByHoursChartCategories}
											series={this.state.traphicByHoursChartSeries} />
									</div>
								</div>
							</div>
							<div className='col-md-4'>
								<div className='panel panel-filled'>
									<div className='panel-body'>
										<PieChart title='Opportunities By Age' data={this.state.opportunitiesAgePieData} />
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>
			</div >
		)
	}
}
