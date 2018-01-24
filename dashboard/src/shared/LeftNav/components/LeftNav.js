import React from 'react'
import './LeftNav.scss'

export const LeftNav = () => {
	return (
		<aside className='navigation'>
			<nav>
				<ul className='nav luna-nav'>
					<li className='nav-category'>
						Menu
						</li>
					<li className='active'>
						<a href='index.html'>Dashboard</a>
					</li>
					<li>
						<a href='#monitoring' data-toggle='collapse' aria-expanded='false'>
							Cameras<span className='sub-nav-icon'> <i className='stroke-arrow' /> </span>
						</a>
					</li>
					<li>
						<a href='#monitoring' data-toggle='collapse' aria-expanded='false'>
							Ad Content<span className='sub-nav-icon'> <i className='stroke-arrow' /> </span>
						</a>
					</li>
					<li>
						<a href='#monitoring' data-toggle='collapse' aria-expanded='false'>
							Settings<span className='sub-nav-icon'> <i className='stroke-arrow' /> </span>
						</a>
					</li>
					<li className='nav-info'>
						<i className='pe pe-7s-shield text-accent' />
						<div className='m-t-xs'>
							<span className='c-white'>Opportunities</span> are a configurable goal to determine when a unique visitor has interacted with the target for a set time.
							Currently the Opportunity interval is set to 10 seconds.
                    </div>
					</li>
					<li className='nav-info'>
						<i className='pe pe-7s-shield text-accent' />
						<div className='m-t-xs'>
							<span className='c-white'>Synaps</span> retail analytics provides retailers a 
							platform to track, measure, and analyze data collected from in-store customer interactions.<br /><br /><a href="http://synapsretail.com">synapsretail.com</a>
                    </div>
					</li>
					
				</ul>
			</nav>
		</aside>
	)
}

export default LeftNav
