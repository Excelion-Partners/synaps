import React from 'react'
import './Header.scss'
import ProfileImage from '../assets/profile.jpg'
import logo from '../assets/synaps.png'

export const Header = () => {
	return (
		<nav className='navbar navbar-default navbar-fixed-top'>
			<div className='container-fluid'>
				<div className='navbar-header'>
					<div id='mobile-menu'>
						<div className='left-nav-toggle'>
							<a href='#'>
								<i className='stroke-hamburgermenu' />
							</a>
						</div>
					</div>
					<a className='logo' href='index.html'>
						<img src={logo} />
					</a>
				</div>
				<div id='navbar' className='navbar-collapse collapse'>
					<ul className='nav navbar-nav navbar-right'>
						<li className='profil-link'>
							<a href='login.html'>
								<span className='profile-address'>demo@synapsretail.com</span>
								<img src={ProfileImage} className='img-circle' alt />
							</a>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}

export default Header
