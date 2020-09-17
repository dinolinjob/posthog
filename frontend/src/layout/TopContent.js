import './TopContent.scss'

import React from 'react'
import { LatestVersion } from '~/layout/LatestVersion'
import { User, Projects, Organization } from '~/layout/TopSelectors'
import { WorkerStats } from '~/layout/WorkerStats'

export function TopContent() {
    return (
        <div>
            <div
                className="layout-top-content right-align"
                style={{
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'center',
                    alignItems: 'center',
                    fontSize: 13,
                }}
            >
                <LatestVersion />
                <WorkerStats />
                <Organization />
                <Projects />
                <User />
            </div>
        </div>
    )
}
