---
name: Bruno Simon — Conhecimento Técnico Completo
description: Three.js, GLSL, R3F, pipeline 3D, performance, frameworks de decisão
type: clone-knowledge
clone: bruno-simon
---

# Conhecimento Técnico Completo — Bruno Simon

> Arquivo central. Tudo que o clone precisa para responder com profundidade técnica em Three.js / WebGL / R3F / GLSL.

---

## 1. Three.js Fundamentals

Toda cena Three.js tem três peças mínimas: **Scene**, **Camera**, **Renderer**.

```javascript
import * as THREE from 'three'

// Scene — o "mundo"
const scene = new THREE.Scene()
scene.background = new THREE.Color(0x050507) // dark o negócio do usuário

// Camera — o "olho"
const camera = new THREE.PerspectiveCamera(
  45,                                   // FOV em graus
  window.innerWidth / window.innerHeight, // aspect
  0.1,                                  // near plane
  100                                   // far plane
)
camera.position.set(3, 2, 5)

// Renderer — o "pintor"
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  powerPreference: 'high-performance',
  alpha: true,
})
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)) // cap em 2 pra não fritar mobile
document.body.appendChild(renderer.domElement)

// Loop
const clock = new THREE.Clock()
function tick() {
  const elapsed = clock.getElapsedTime()
  const delta = clock.getDelta()
  renderer.render(scene, camera)
  requestAnimationFrame(tick)
}
tick()
```

**Cuidado de iniciante**: nunca use `Date.now()` ou `performance.now()` como base de tempo da animação — use `clock.getDelta()`. Isso normaliza o framerate e evita que sua animação fique mais rápida em monitor 144Hz.

---

## 2. Geometry — sempre BufferGeometry

`Geometry` (a antiga) foi removida no Three r125. Hoje só existe `BufferGeometry` — mais rápida, menos memória, contrato direto com WebGL.

```javascript
// Primitivas prontas
const sphere = new THREE.SphereGeometry(1, 32, 32) // radius, widthSegments, heightSegments
const box   = new THREE.BoxGeometry(1, 1, 1)
const plane = new THREE.PlaneGeometry(2, 2, 64, 64) // segments altos pra vertex shader

// Geometry custom (raro, mas vale conhecer)
const geometry = new THREE.BufferGeometry()
const positions = new Float32Array([
  0, 0, 0,
  1, 0, 0,
  0, 1, 0,
])
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
```

**Heurística**: para cenas onde você vai aplicar vertex shader, **suba os segments**. Plane padrão (1,1) tem 4 vértices — vertex displacement não vai aparecer. Use 64x64 ou 128x128.

---

## 3. Materials — qual usar quando

| Material | Quando usar | Custo |
|---|---|---|
| `MeshBasicMaterial` | Sem luz, debug, UI 3D | Baixíssimo |
| `MeshStandardMaterial` | PBR padrão, 90% dos casos | Médio |
| `MeshPhysicalMaterial` | Vidro, clearcoat, transmission | Alto |
| `MeshNormalMaterial` | Debug visual (mostra normais) | Baixo |
| `ShaderMaterial` | Custom shader, controle total | Você quem manda |
| `RawShaderMaterial` | Shader sem includes Three | Você quem manda |
| `MeshToonMaterial` | Estilo cel-shading | Médio |

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xC9A84C,        // gold o negócio do usuário
  roughness: 0.4,
  metalness: 0.8,
  envMapIntensity: 1.5,
})
```

**Regra do Bruno**: comece com `MeshStandardMaterial` + um `<Environment>` HDR. Se não estiver bonito, o problema raramente é o material — é a iluminação ou a textura.

---

## 4. Lights & Shadows

```javascript
// Ambient — preenchimento, sem direção
const ambient = new THREE.AmbientLight(0xffffff, 0.4)
scene.add(ambient)

// Directional — sol
const sun = new THREE.DirectionalLight(0xffffff, 1.5)
sun.position.set(5, 10, 7.5)
sun.castShadow = true
sun.shadow.mapSize.set(1024, 1024) // 2048 se desktop bom, 512 se mobile
sun.shadow.camera.near = 0.1
sun.shadow.camera.far = 50
sun.shadow.camera.left = -10
sun.shadow.camera.right = 10
sun.shadow.camera.top = 10
sun.shadow.camera.bottom = -10
scene.add(sun)

// Renderer
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFSoftShadowMap

// Mesh
mesh.castShadow = true
mesh.receiveShadow = true
```

**Cuidado**: cada DirectionalLight com sombra adiciona um **render extra da cena** sob a perspectiva da luz. Isso é caro. Em mobile, **uma luz com sombra**, ponto. O resto sem sombra.

Alternativa profissional: **bake** a iluminação no Blender (Cycles → AO + ColorMap) e use `MeshBasicMaterial` com a textura bakeada. Cena fica linda, custo zero em runtime.

---

## 5. GLSL — Shaders na unha

### Mental model
- **Vertex shader** roda **uma vez por vértice**. Decide onde o vértice aparece na tela. Saída obrigatória: `gl_Position`.
- **Fragment shader** roda **uma vez por pixel renderizado**. Decide a cor. Saída obrigatória: `gl_FragColor` (em GLSL ES 1.0, padrão Three.js) ou variável `out` (GLSL ES 3.0).

### Anatomia básica

**Vertex shader**:
```glsl
uniform float uTime;
varying vec2 vUv;
varying vec3 vNormal;

void main() {
  vUv = uv;
  vNormal = normal;

  vec3 newPosition = position;
  newPosition.y += sin(uTime + position.x * 5.0) * 0.2;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
}
```

**Fragment shader**:
```glsl
uniform vec3 uColorA;
uniform vec3 uColorB;
varying vec2 vUv;

void main() {
  vec3 color = mix(uColorA, uColorB, vUv.y);
  gl_FragColor = vec4(color, 1.0);
}
```

**Material**:
```javascript
const material = new THREE.ShaderMaterial({
  vertexShader,
  fragmentShader,
  uniforms: {
    uTime:   { value: 0 },
    uColorA: { value: new THREE.Color(0xC9A84C) },
    uColorB: { value: new THREE.Color(0x050507) },
  },
})

// Update no tick
material.uniforms.uTime.value = clock.getElapsedTime()
```

### Patterns úteis

**Smoothstep gradient**:
```glsl
float t = smoothstep(0.2, 0.8, vUv.y);
vec3 color = mix(colorBottom, colorTop, t);
```

**Distance to mouse (fragment)**:
```glsl
uniform vec2 uMouse;
varying vec2 vUv;

void main() {
  float d = distance(vUv, uMouse);
  float glow = 1.0 - smoothstep(0.0, 0.3, d);
  gl_FragColor = vec4(vec3(glow), 1.0);
}
```

**Noise (simplex 2D, cole sem pensar)**:
```glsl
// Ashima Arts — Simplex 2D, copy-paste sem culpa
vec3 mod289(vec3 x) { return x - floor(x * (1.0/289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0/289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                     -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod289(i);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
              + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
                          dot(x12.zw,x12.zw)), 0.0);
  m = m*m; m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
```

### Mantra do shader
- **Vertex**: "onde esse vértice vai aparecer?"
- **Fragment**: "qual cor esse pixel tem?"
- **Uniform**: "valor único pra todos os pixels/vértices, vindo do JS"
- **Attribute**: "valor por vértice (posição, normal, uv)"
- **Varying**: "ponte vertex→fragment, interpolada"

---

## 6. React Three Fiber (R3F)

R3F = Three.js declarativo dentro de React. Mesma API, sintaxe JSX.

```jsx
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import { useRef } from 'react'

function SpinningBox() {
  const ref = useRef()
  useFrame((state, delta) => {
    ref.current.rotation.y += delta * 0.5
  })
  return (
    <mesh ref={ref}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#C9A84C" metalness={0.8} roughness={0.4} />
    </mesh>
  )
}

export default function Scene() {
  return (
    <Canvas
      camera={{ position: [3, 2, 5], fov: 45 }}
      dpr={[1, 2]}
      gl={{ antialias: true, powerPreference: 'high-performance' }}
    >
      <Environment preset="studio" />
      <SpinningBox />
      <OrbitControls />
    </Canvas>
  )
}
```

### Drei — helpers essenciais
- `<OrbitControls />` — câmera orbital
- `<Environment preset="..." />` — HDR pré-definido (studio, sunset, city, dawn, night...)
- `<Float />` — flutuação suave automática
- `<Text />` — texto 3D
- `<useGLTF />` — carregar modelo glTF
- `<MeshTransmissionMaterial />` — vidro real (refração)
- `<Instances>` / `<Instance>` — instancing declarativo
- `<Bvh />` — raycast acelerado
- `<Html />` — HTML dentro da cena 3D

### Performance no R3F

```jsx
<Canvas frameloop="demand"> {/* só renderiza quando algo muda */}
```

Use `frameloop="demand"` para cenas estáticas com interação ocasional. Reduz drasticamente uso de GPU.

`useMemo` para criar geometrias/materiais uma vez:
```jsx
const geometry = useMemo(() => new THREE.SphereGeometry(1, 32, 32), [])
```

---

## 7. Physics — Rapier (preferido) ou Cannon (legado)

**Rapier** (Rust + WASM, manutenção ativa):

```jsx
import { Physics, RigidBody } from '@react-three/rapier'

<Physics gravity={[0, -9.81, 0]}>
  <RigidBody type="dynamic" colliders="ball">
    <mesh position={[0, 5, 0]}>
      <sphereGeometry args={[0.5]} />
      <meshStandardMaterial color="gold" />
    </mesh>
  </RigidBody>
  <RigidBody type="fixed">
    <mesh rotation={[-Math.PI/2, 0, 0]}>
      <planeGeometry args={[10, 10]} />
      <meshStandardMaterial color="#111" />
    </mesh>
  </RigidBody>
</Physics>
```

**Quando usar physics**: só quando a interação física é **o ponto da experiência** (carrinho do bruno-simon.com, dominó interativo, físicas de bola). Para 95% das landing pages, simule o efeito com `lerp` + easing — fica igual e custa zero.

```javascript
// Lerp manual — substitui physics quando você só quer "movimento natural"
useFrame((state, delta) => {
  ref.current.position.x = THREE.MathUtils.lerp(
    ref.current.position.x,
    targetX,
    delta * 4 // velocidade de aproximação
  )
})
```

---

## 8. Pipeline 3D — Blender → glTF → web

1. **Modela em Blender** (gratuito, padrão indústria web 3D)
2. **Bake lighting** se a cena é estática (Cycles → AO + ColorMap em uma textura única)
3. **Exporta glTF binário** (`.glb`) — formato mais leve, suporta animação, materiais PBR, texturas embutidas
4. **Comprime** com `gltf-transform`:
   ```bash
   npx @gltf-transform/cli optimize input.glb output.glb \
     --texture-compress webp \
     --simplify-error 0.001
   ```
5. **Texturas em KTX2** (Basis Universal): 5-10x menos peso que PNG, decodifica direto na GPU
6. **Carrega no R3F**:
   ```jsx
   import { useGLTF } from '@react-three/drei'
   const { scene } = useGLTF('/model.glb')
   return <primitive object={scene} />
   ```

**Heurística**: o asset bem otimizado pesa <500KB. Se o seu glTF passa de 2MB, você não otimizou — você só exportou.

---

## 9. Post-processing — EffectComposer

```jsx
import { EffectComposer, Bloom, DepthOfField, Vignette } from '@react-three/postprocessing'

<Canvas>
  <Scene />
  <EffectComposer>
    <Bloom intensity={1.5} luminanceThreshold={0.6} luminanceSmoothing={0.025} mipmapBlur />
    <DepthOfField focusDistance={0.01} focalLength={0.05} bokehScale={4} />
    <Vignette offset={0.3} darkness={0.7} />
  </EffectComposer>
</Canvas>
```

**Cuidado**: cada pass = um render full-screen extra. Em mobile, **desabilite postprocessing** ou simplifique para vignette só:

```jsx
const isMobile = useMediaQuery('(max-width: 768px)')
{!isMobile && <EffectComposer>...</EffectComposer>}
```

---

## 10. Performance — Frameworks de decisão

### Frame budget mental
- 16.6ms por frame para 60fps
- 33.3ms por frame para 30fps (mínimo aceitável)
- Subtrai overhead do JS — você tem **~10ms para a GPU** num app real

### O que mais pesa (em ordem)
1. **Sombras dinâmicas** — render extra da cena por luz com `castShadow`
2. **Postprocessing passes** — render full-screen por pass
3. **Transparência sobreposta** — cada layer transparente força reordenação
4. **Materiais Physical com transmission** — caríssimo
5. **Geometria com muitos vértices** — só nota acima de ~2M

### Otimizações na ordem certa

```javascript
// 1. Cap pixel ratio (mobile mata aqui)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

// 2. Frustum culling automático — confira que está ativo
mesh.frustumCulled = true

// 3. Instancing pra repetições
const instancedMesh = new THREE.InstancedMesh(geometry, material, 1000)
for (let i = 0; i < 1000; i++) {
  matrix.setPosition(Math.random()*10, 0, Math.random()*10)
  instancedMesh.setMatrixAt(i, matrix)
}

// 4. LOD (Level of Detail)
const lod = new THREE.LOD()
lod.addLevel(highDetailMesh, 0)
lod.addLevel(mediumDetailMesh, 10)
lod.addLevel(lowDetailMesh, 50)
scene.add(lod)

// 5. Bake luz quando estático
// (no Blender, não em runtime)

// 6. Compressão de texturas KTX2
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js'
```

### Diagnóstico
```javascript
console.log(renderer.info.render)
// {
//   calls: 47,         // draw calls — alvo < 100
//   triangles: 235000, // alvo < 500k mobile, < 2M desktop
//   points: 0,
//   lines: 0,
//   frame: 1234,
// }
```

---

## 11. Frameworks de decisão (opiniões fortes)

### "3D site decision tree" — a pergunta antes da pergunta

```
A experiência só faz sentido em 3D?
├─ SIM → Three.js / R3F faz sentido
│   ├─ Time é React? → R3F
│   └─ Time é vanilla / cena gigante? → Three.js puro
└─ NÃO → use o que custa menos
    ├─ Decoração → CSS + SVG + Lottie
    ├─ Animação simples → GSAP / Framer Motion
    └─ Background animado → canvas 2D ou shader fullscreen
```

### "Quando NÃO usar 3D"
- Landing page de serviço (manutenção PC, restaurante, dentista) — **CSS + bom design entrega o mesmo impacto**
- Site institucional onde o conteúdo é texto e foto — **3D vira distração**
- Mobile-first com público de baixa renda (smartphones de entrada) — **3D vai engasgar**
- Time pequeno sem dev WebGL — **manutenção vira pesadelo**

### "R3F vs Three.js puro"
- **R3F vence** quando: time React, integração com state (Zustand, Redux), composição declarativa, hot reload importa
- **Three puro vence** quando: cena gigante e complexa com muito controle imperativo, time vanilla JS, integração com lib não-React (vanilla GSAP), build size é crítico

### "Blender vs Cinema4D vs Maya"
- **Blender**: gratuito, padrão de fato da web 3D, comunidade gigante, exporta glTF nativo. **Use Blender**.
- Cinema4D / Maya: caros, ótimos pra motion design e VFX, mas o pipeline pra web é mais chato. Use só se você já vem desse mundo.

---

## 12. Checklist final pra qualquer cena 3D web

Antes de considerar "pronta":
- [ ] Cap em `dpr` (max 2)
- [ ] `frustumCulled = true` em meshes (default já é, mas confira)
- [ ] glTF comprimido (<500KB ideal)
- [ ] Texturas em KTX2 ou WebP
- [ ] Sombras só onde nota
- [ ] Postprocessing simplificado (ou off) em mobile
- [ ] Loading screen com progresso real
- [ ] Fallback se WebGL não disponível (raro hoje, mas exists)
- [ ] Testado em mobile real (não DevTools)
- [ ] `renderer.info.render.calls` < 100
- [ ] 60fps em desktop, 30fps+ em mobile médio

Se passou em todos: **ship**.
