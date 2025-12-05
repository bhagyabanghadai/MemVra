import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial, Float, ScrollControls, useScroll, Environment } from '@react-three/drei';
import * as THREE from 'three';

function DigitalEntity() {
    const pointsRef = useRef<THREE.Points>(null);
    const scroll = useScroll();

    // Generate particles
    const particles = useMemo(() => {
        const count = 5000;
        const positions = new Float32Array(count * 3);
        const colors = new Float32Array(count * 3);
        const color1 = new THREE.Color("#22d3ee"); // Cyan
        const color2 = new THREE.Color("#3b82f6"); // Blue

        for (let i = 0; i < count; i++) {
            const r = (Math.random() - 0.5) * 10;
            const theta = 2 * Math.PI * Math.random();
            const phi = Math.acos(2 * Math.random() - 1);

            const x = r * Math.sin(phi) * Math.cos(theta);
            const y = r * Math.sin(phi) * Math.sin(theta);
            const z = r * Math.cos(phi);

            positions[i * 3] = x;
            positions[i * 3 + 1] = y;
            positions[i * 3 + 2] = z;

            // Mix colors
            const mixedColor = color1.clone().lerp(color2, Math.random());
            colors[i * 3] = mixedColor.r;
            colors[i * 3 + 1] = mixedColor.g;
            colors[i * 3 + 2] = mixedColor.b;
        }
        return { positions, colors };
    }, []);

    useFrame((_state, delta) => {
        if (!pointsRef.current) return;

        // Get scroll offset (0 to 1)
        const r1 = scroll.range(0, 1 / 3);
        const _r2 = scroll.range(1 / 3, 1 / 3);
        const r3 = scroll.range(2 / 3, 1 / 3);

        // Base rotation
        pointsRef.current.rotation.x -= delta * 0.1;
        pointsRef.current.rotation.y -= delta * 0.15;

        // Scroll-based transformations
        // Phase 1: Sphere -> Explode
        // Phase 2: Explode -> Tunnel/Ring

        // @ts-ignore - THREE.js types are strict but this works at runtime
        const _positions = pointsRef.current.geometry.attributes.position.array as Float32Array;

        // Simple morphing simulation by scaling
        // Ideally we would interpolate between pre-calculated shapes, 
        // but for this demo we'll manipulate the object scale and rotation speed.

        const scale = 1 + r1 * 2 - r3 * 1; // Expand then contract
        pointsRef.current.scale.set(scale, scale, scale);

        // Rotation speed increases with scroll
        pointsRef.current.rotation.z = scroll.offset * Math.PI * 2;
    });

    return (
        <group rotation={[0, 0, Math.PI / 4]}>
            <Points ref={pointsRef} positions={particles.positions} colors={particles.colors} stride={3} frustumCulled={false}>
                <PointMaterial
                    transparent
                    vertexColors
                    size={0.05}
                    sizeAttenuation={true}
                    depthWrite={false}
                    blending={THREE.AdditiveBlending}
                />
            </Points>
        </group>
    );
}

export default function Scene3D() {
    return (
        <div className="fixed inset-0 z-0 pointer-events-none">
            <Canvas camera={{ position: [0, 0, 6], fov: 60 }}>
                <color attach="background" args={['#000000']} />
                <ambientLight intensity={0.5} />
                <ScrollControls pages={3} damping={0.2}>
                    {/* The 3D content that reacts to scroll */}
                    <Float speed={2} rotationIntensity={1} floatIntensity={1}>
                        <DigitalEntity />
                    </Float>
                </ScrollControls>
                <Environment preset="city" />
            </Canvas>
        </div>
    );
}
