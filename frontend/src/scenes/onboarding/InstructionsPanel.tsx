import { CardContainer } from 'scenes/onboarding/CardContainer'
import {
    AndroidInstructions,
    APIInstructions,
    ElixirInstructions,
    FlutterInstructions,
    GoInstructions,
    IOSInstructions,
    JSInstructions,
    NodeInstructions,
    PHPInstructions,
    PythonInstructions,
    RNInstructions,
    RubyInstructions,
} from 'scenes/onboarding/FrameworkInstructions'
import { Row } from 'antd'
import React from 'react'
import { API, MOBILE, PURE_JS, WEB } from 'scenes/onboarding/constants'
import { Framework, PlatformType } from 'scenes/onboarding/types'

const frameworksSnippet = {
    PURE_JS: JSInstructions,
    NODEJS: NodeInstructions,
    GO: GoInstructions,
    RUBY: RubyInstructions,
    PYTHON: PythonInstructions,
    PHP: PHPInstructions,
    ELIXIR: ElixirInstructions,
    ANDROID: AndroidInstructions,
    IOS: IOSInstructions,
    REACT_NATIVE: RNInstructions,
    FLUTTER: FlutterInstructions,
    API: APIInstructions,
}

export function InstructionsPanel({
    onSubmit,
    reverse,
    platformType,
    framework,
}: {
    onSubmit: ({ type, framework }: { type?: PlatformType; framework?: Framework }) => void
    reverse: () => void
    platformType: PlatformType
    framework: Framework
}): JSX.Element {
    if (!framework) {
        return <></>
    }

    const FrameworkSnippet = frameworksSnippet[framework]

    if (framework === API) {
        return (
            <CardContainer index={2} totalSteps={4} nextButton={true} onSubmit={onSubmit} onBack={reverse}>
                <h2>API</h2>
                <p className="prompt-text">
                    {
                        "Below is an easy format for capturing events using the API we've provided. Use this endpoint to send your first event!"
                    }
                </p>
                <FrameworkSnippet />
            </CardContainer>
        )
    }

    if (framework === PURE_JS) {
        return (
            <CardContainer index={2} totalSteps={4} nextButton={true} onSubmit={onSubmit} onBack={reverse}>
                <h2>posthog-js</h2>
                <p className="prompt-text">
                    {
                        'posthog-js will automatically capture page views, page leaves, and interactions with specific elements (<a>, <button>, <input>, <textarea>, <form>)'
                    }
                </p>
                <FrameworkSnippet />
            </CardContainer>
        )
    }

    return (
        <CardContainer index={2} totalSteps={4} nextButton={true} onSubmit={onSubmit} onBack={reverse}>
            {platformType === WEB ? (
                <Row style={{ marginLeft: -5 }} justify="space-between" align="middle">
                    <h2 style={{ color: 'black', marginLeft: 8 }}>{'Custom Capture'}</h2>
                </Row>
            ) : (
                <h2>Setup</h2>
            )}
            {platformType === WEB ? (
                <>
                    <p className="prompt-text">
                        {
                            'To send events from your backend or add custom events, you can use our framework specific libraries.'
                        }
                    </p>
                    <FrameworkSnippet />
                </>
            ) : null}
            {platformType === MOBILE ? <FrameworkSnippet /> : null}
        </CardContainer>
    )
}
