---
title: Fusion 360: Basics
date: 2019-11-12
tag: 3D Modeling
---

A brief notes for basic [Fusion 360](https://www.autodesk.co.kr/products/fusion-360/overview) usage. I'll go through the commonly used features in the top navigation bar, focused on the core workflow: sketch → solid modeling → STL export.

![Fusion 360 overview as of Nov 14, 2019](img/posts/191112-fusion-360-basics/overview.jpg)

# SOLID Tab

![](img/posts/191112-fusion-360-basics/solid-tab.jpg)

The default tab. The basic workflow goes: 1) Click Create Sketch (the leftmost icon with a plus sign) to enter the SKETCH tab. 2) Draw a 2D shape, then click Finish Sketch to return. 3) Use Extrude or similar tools to create a 3D structure. Most modeling work is just repeating this cycle.

## CREATE

- **Extrude** — Beginners mainly use this. Select a sketched face, click Extrude, set the depth, and the 2D face becomes a 3D solid. The Operation option lets you choose Join (merge with existing body), Cut (carve into existing body), or New Body (create an independent body), so cutting holes and joining parts all go through Extrude.
- **Revolve** — Recently used this for the first time. Select a face, click the axis line to revolve around, set the angle, and the face sweeps around the axis to form a solid.
- **Box, Cylinder, Sphere, etc.** — These let you create 3D primitives directly without sketching a 2D plane first.

## MODIFY

- **Fillet** — Most of what I use from the Modify menu. Click an edge and apply Fillet to round it. Example below.

![|30%](img/posts/191112-fusion-360-basics/fillet.jpg)

- **Scale** — Resize a solid body while maintaining its proportions.

## CONSTRUCT

Creates a 2D sketch plane at a desired position. You can place a new sketch plane on an existing face or at a set distance from one. Becomes increasingly important as models get more complex.

## INSPECT

- Click INSPECT, then click two points to measure the distance between them.
  - Works for point-to-point, point-to-edge, point-to-face (shortest distance), face-to-face (perpendicular distance), etc.
- Fairly high usage frequency.

# SKETCH Tab

![](img/posts/191112-fusion-360-basics/sketch-tab.jpg)

## CREATE

- **Line (L), Circle (C), Rectangle (R)** — The three I use most. Letters in parentheses are shortcuts. Click the reference points needed for the shape and Fusion draws it.
- **Arc, Polygon, Spline, etc.** — Used occasionally. Haven't touched Spline yet.

## CONSTRUCTION

Toggling Construction mode draws shapes as dashed construction lines instead of solid lines. They don't affect the model and serve only as reference geometry. Useful for spacing, e.g., placing a circle exactly 40mm from another circle's center.

![|40%](img/posts/191112-fusion-360-basics/constraints.jpg)

## FINISH SKETCH

Closes the current sketch. Simple feature, but using it properly to keep the Timeline clean is important.

# Timeline and Component Tree

## Component Tree

Stores the origin axes, model bodies, and sketches. Click the eye icon next to any element to show or hide it. The Timeline is auto-generated based on these components.

![|40%](img/posts/191112-fusion-360-basics/component-tree.jpg)

## Timeline

The Timeline sits at the bottom of the screen. As a project grows and more people collaborate, clean version management matters. Like Git commits, you can roll back to an earlier state if something goes wrong. Managing the Timeline well seems to be one of the most important habits in Fusion 360.

![](img/posts/191112-fusion-360-basics/timeline.jpg)

Example: if you want to add geometry to a sketch plane you created earlier, don't create a new sketch plane. Instead, find the original sketch in the Component tree, double-click it to re-enter it, and draw there. This keeps the Timeline from getting tangled. Renaming sketches by double-clicking (e.g., Sketch1 → base_profile) makes them much easier to find later.

# TOOLS Tab

![](img/posts/191112-fusion-360-basics/tools-tab.jpg)

This is where you export to `.stl`. Steps: 1) Select the body to export from the Component tree or viewport. 2) Click TOOLS → MAKE → 3D Print. 3) Uncheck "Send to 3D Print Utility" in the right panel if you want to save a file rather than open an external slicer. 4) Click OK and choose a save location.

# Changelog
- Nov 12, 2019: Post published
- Dec 1, 2021: Migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
