import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
    title: 'DS Research Agent',
    description: 'Data Science Research Assistant powered by Gemini',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}
