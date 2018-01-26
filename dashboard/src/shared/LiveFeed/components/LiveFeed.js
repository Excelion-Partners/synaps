import React from 'react'
import './LiveFeed.scss'

export class LiveFeed extends React.Component {

	constructor(props) {
		super(props)

		var socket = io.connect('http://localhost:3001')

		this.state = {
			binData: 'test'
		}

		var self = this

		socket.on('frame', function (data) {
			self.state.binData = null;
			self.forceUpdate();
			//console.log('frame received : ' + data.buffer);
			// img.onload = function () {
			// 	context.drawImage(this, 0, 0, canvas.width, canvas.height);
			// };
			//img.src = 'data:image/png;base64,' + data.buffer;
			self.state.binData = null;
			self.state.binData = data.buffer;
			self.forceUpdate();
		});
	}

	render() {
		var label = {
			color: '#f2f2f2',
			fontSize: '22px',
			textAlign: 'center'
		}

		var vidPadding = {
			paddingTop: '15px'
		}

		// var video = {
		// 	width: '600px',
		// 	display: 'block',
		// 	marginLeft: '100px',
		// 	marginTop: '15px'
		// }

		return ( <
			div >
			<
			div style = {
				label
			} > Live Feed(DEMO): < /div> <
			div style = {
				vidPadding
			} >
			<
			img className = 'img-responsive'
			src = {
				"data:image/png;base64," + this.state.binData
			}
			/> < /
			div > <
			/div>
		)
	}
}

export default LiveFeed
