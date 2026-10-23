# Skeleton

A placeholder block that mimics the shape of content while it loads. Match each skeleton's size and shape to the real content as closely as possible to keep layout shift minimal.

## Notes

- Skeleton works because mirroring the expected layout reduces perceived load time — that is the core reason to prefer Skeleton over Spinner when the layout is known.

- Use Spinner (not Skeleton) when the layout of the loading content is unknown. Skeleton only pays off when its shapes mirror the real content.

- Match skeleton shapes to the real content as closely as possible — mismatched shapes cause a jarring layout shift when real content loads.

- Use ProgressBar (not Skeleton) when the operation has a measurable percentage.

- Skip the skeleton for very fast loads (under ~200ms) — it flickers in and out and adds visual noise without reducing perceived load time.

## Examples

### Kinds Skeleton

Pick a `kind` to match the shape of the content being loaded: `line` (default) for single-line text, `pill` for tags or badges, and `circle` for avatars or icons.

```tsx
<Stack gap="density-md">
  <Skeleton kind="circle" />
  <Skeleton kind="pill" />
  <Skeleton kind="line" />
  <Skeleton kind="line" />
</Stack>
```

### Static Skeleton

Set `animated={false}` when the skeleton flashes briefly or sits inside a surface that already conveys a loading state, where the pulse would be visual noise.

```tsx
<Skeleton kind="line" animated={false} />
```

### Inline Text Skeleton

By default, the skeleton will inherit the surrounding font size — ideal for swapping in for a heading or label while its data resolves.

```tsx
<Text kind="title/lg">
  <Skeleton />
</Text>
```

### Sized Skeleton

Override the default dimensions with `className` or `style` so the skeleton matches the exact size of the component it stands in for, like a large `Avatar` or icon.

```tsx
<Skeleton kind="circle" className="size-12" />
```

### Content Block Skeleton

Compose multiple skeleton shapes inside layout primitives to mirror the rough size and rhythm of a content block so the page does not jump when real data loads in.

```tsx
<Stack gap="density-lg" style={{ maxWidth: "320px" }}>
  <Skeleton kind="circle" />
  <Skeleton kind="line" style={{ width: "66%" }} />
  <Stack gap="density-sm">
    <Skeleton kind="line" />
    <Skeleton kind="line" />
    <Skeleton kind="line" />
  </Stack>
  <Flex gap="density-sm" wrap="wrap">
    <Skeleton kind="pill" />
    <Skeleton kind="pill" />
  </Flex>
</Stack>
```

## Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| animated | `boolean` | `true` | Whether the skeleton pulses while visible. |
| asChild | `boolean` | - | Render-as-child slot (from Radix Primitive) |
| kind | `"circle" \| "line" \| "pill"` | `"line"` | Shape of the placeholder. Pick the option that most closely matches the content it stands in for. - "line" - Text-shaped block whose height scales with the surrounding font size. - "pill" - Fixed-width rounded rectangle for tag- or chip-like content. - "circle" - Fixed-diameter circle for avatars and icons. |

## Exports

- Components: `Skeleton`
- Types: `SkeletonProps`
