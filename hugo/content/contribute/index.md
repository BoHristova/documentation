---
aside: false
description: Contributor guides for code and documentation
persona: Developers
title: Contribute
weight: 110
prev: false
next: false
---
<!-- BANNER:LOCAL -->
<!--
   █▀█ █▄▀
   █ █ █▀▄
   ▀▀▀ ▀ ▀

   ┌────────────────────────────────────────────────┐
   │  LOCAL FILE — maintained in gardener/            │
   │  documentation.                                  │
   │                                                  │
   │  Go ahead and edit this file directly.           │
   │  Changes here are the source of truth.           │
   └────────────────────────────────────────────────┘
-->


# Welcome to the Contributor Page of Gardener

This page is your starting point for contributing to Gardener. It contains all documentation related to developing and documenting Gardener.

We appreciate all kinds of contributions – from fixing a typo to implementing a new feature. Let's grow Gardener together!

## Get Started

<CardGrid :columns="2" :cards="[
{
title: 'Contribution Process',
details: 'Learn how to contribute to Gardener, including contribution workflows, licensing requirements, and best practices.',
link: '/contribute/contribution-process/'
},
{
title: 'Developer Starter Kit',
details: 'Set up and deploy Gardener locally. Explore key development guidelines, such as testing, validation, and dependency management guidelines.',
link: '/contribute/developer-starter-kit/'
}
]"/>

## Contribute to a Specific Area

<CardGrid :cards="[
{
title: 'Gardener Core',
details: 'Browse the developer docs for the core Gardener functionality – development and contribution guidelines, information about networking, observability, and more.',
link: '/contribute/gardener/'
},
{
title: 'Extensions',
sections: [
  { details: 'Learn how to build a new Gardener extension – CRD conventions, health checks, admission webhooks, and lifecycle management.', link: '/contribute/build-extensions/', linkText: 'Build a Gardener extension' },
  { details: 'Browse the developer docs for the Gardener extensions for infrastructure providers, Kubernetes auditing, DNS services, and others.', link: '/contribute/extensions/', linkText: 'Contribute to an existing extension' }
]
},
{
title: 'Other Components',
details: 'Browse the developer docs for components such as Dependency Watchdog, etcd-druid, and Machine Controller Manager.',
link: '/contribute/other-components/'
},
{
title: 'Dashboard',
details: 'Browse the developer docs for the Gardener web UI – architecture, local development setup, and testing guidelines.',
link: '/contribute/dashboard/'
},
{
title: 'Documentation',
details: 'Browse the guidelines for contributing documentation – writing style, structure, tooling, and how to add or update content.',
link: '/contribute/documentation/'
}
]"/>
