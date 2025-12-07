"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial } from "@react-three/drei";
import * as random from "maath/random/dist/maath-random.esm"; // Create a type declaration if needed or ignore type for now

function Stars(props: any) {
    const ref = useRef<any>();
    // Generate 5000 points in a sphere
    const sphere = useMemo(() => random.inSphere(new Float32Array(5000), { radius: 1.5 }), []);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.x -= delta / 10;
            ref.current.rotation.y -= delta / 15;
        }
    });

    return (
        <group rotation={[0, 0, Math.PI / 4]}>
            <Points ref={ref} positions={sphere} stride={3} frustumCulled={false} {...props}>
                <PointMaterial
                    transparent
                    color="#3b82f6" // blue-500
                    size={0.002}
                    sizeAttenuation={true}
                    depthWrite={false}
                />
            </Points>
        </group>
    );
}

function Connections() {
    const ref = useRef<any>();
    // Generate fewer points for a "network" look
    const sphere = useMemo(() => random.inSphere(new Float32Array(300), { radius: 1.2 }), []);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.x += delta / 20;
            ref.current.rotation.y += delta / 25;
        }
    });

    return (
        <group rotation={[0, 0, Math.PI / 3]}>
            <Points ref={ref} positions={sphere} stride={3} frustumCulled={false}>
                <PointMaterial
                    transparent
                    color="#22d3ee" // cyan-400
                    size={0.003}
                    sizeAttenuation={true}
                    depthWrite={false}
                />
            </Points>
        </group>
    );
}

export default function Background3D() {
    return (
        <div className="fixed inset-0 z-[-1] pointer-events-none opacity-60">
            <Canvas
                camera={{ position: [0, 0, 1] }}
                gl={{ antialias: true, alpha: true }}
                dpr={[1, 2]} // Optimize for pixel ratio
            >
                <Stars />
                <Connections />
            </Canvas>
        </div>
    );
}
