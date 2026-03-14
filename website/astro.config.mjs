// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

// https://astro.build/config
export default defineConfig({
	site: 'https://mkmurali.github.io',
	base: '/agentic-ai-workshop-march-2026',
	outDir: '../docs',
	build: {
		assets: '_astro',
	},
	trailingSlash: 'always',
	integrations: [
		mermaid({
			// Auto-switch between light/dark themes
			autoTheme: true,
			mermaidConfig: {
				look: 'handDrawn',
				flowchart: { curve: 'basis' },
			},
		}),
		starlight({
			title: 'Agentic π Day Workshop',
			description: 'Build production AI agents with Strands Agents SDK and AWS AgentCore',
			customCss: ['./src/styles/custom.css'],
			components: {
				Footer: './src/components/overrides/Footer.astro',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/mkmurali/agentic-ai-workshop-march-2026' },
			],
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Welcome', slug: 'index' },
						{ label: 'Environment Setup', slug: 'getting-started/setup' },
					],
				},
				{
					label: 'Concepts',
					items: [
						{ label: 'Introduction to Agentic AI', slug: 'concepts/intro-to-agentic-ai' },
						{ label: 'Architecture Overview', slug: 'concepts/architecture' },
						{ label: 'Strands Agents SDK', slug: 'concepts/strands-sdk' },
					],
				},
				{
					label: 'Workshop Modules',
					items: [
						{ label: 'Module 1: Your First Agent', slug: 'modules/01-first-agent' },
						{ label: 'Module 2: Custom Tools & MCP', slug: 'modules/02-tools-mcp' },
						{ label: 'Module 3: Memory & Context', slug: 'modules/03-memory-context' },
						{ label: 'Module 4: Multi-Agent Patterns', slug: 'modules/04-multi-agent' },
						{ label: 'Module 5: Evals & Safety', slug: 'modules/05-evals-safety' },
						{ label: 'Module 6: Deploy to AWS', slug: 'modules/06-deploy' },
					],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'Workshop Outline', slug: 'reference/outline' },
						{ label: 'Resources & Links', slug: 'reference/resources' },
					],
				},
			],
		}),
	],
});
