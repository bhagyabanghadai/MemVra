import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshTransmissionMaterial, Float, Environment, Lightformer } from '@react-three/drei';
import * as THREE from 'three';

function Crystal() {
    const mesh = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (!mesh.current) return;
        mesh.current.rotation.x = state.clock.elapsedTime * 0.2;
        mesh.current.rotation.y = state.clock.elapsedTime * 0.1;
    });

    return (
        <group dispose={null}>
            <Float speed={2} rotationIntensity={1.5} floatIntensity={2}>
                <mesh ref={mesh} scale={1.5}>
                    <icosahedronGeometry args={[1, 0]} />
                    <MeshTransmissionMaterial
                        backside
                        samples={4}
                        resolution={256}
                        thickness={0.2}
                        roughness={0.0}
                        anisotropy={0.1}
                        chromaticAberration={0.05}
                        color="#ffffff"
                    />
                </mesh>
            </Float>
        </group>
    );
}

export default function CrystalScene() {
    return (
        <div className="absolute inset-0 z-0">
            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                <color attach="background" args={['#050505']} />
                <ambientLight intensity={0.5} />
                <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} />
                <Crystal />
                <Environment preset="city">
                    <Lightformer intensity={8} position={[10, 5, 0]} scale={[10, 50, 1]} onUpdate={(self) => self.lookAt(0, 0, 0)} />
                </Environment>
            </Canvas>
        </div>
    );
}
