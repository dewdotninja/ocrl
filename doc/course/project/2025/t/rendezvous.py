import numpy as np
import meshcat as mc
import meshcat.geometry as geom
import meshcat.transformations as tf
import os


# =========================
# CREATE CIRCLE
# =========================
def create_circle(N_circ):
    R = 1.1
    theta_vec = np.linspace(0 - np.pi/2, 2*np.pi + np.pi/2, N_circ)

    circle = []
    for theta in theta_vec:
        circle.append(np.array([
            R*np.cos(theta),
            -3,
            R*np.sin(theta) + 3
        ]))

    return circle


# =========================
# DESIRED TRAJECTORY
# =========================
def desired_trajectory(x0, xg, N, dt):

    N_circle = 65
    N_pre = 10
    N_post = 25

    p_circle = create_circle(N_circle)

    p_pre_circle = np.linspace(x0[0:3], p_circle[0], N_pre + 1)

    p_post1 = np.linspace(p_circle[-1], np.array([xg[0], -3, xg[2]]), 9)
    p_post2 = np.linspace(np.array([xg[0], -3, xg[2]]), xg[0:3], 18)

    p_post_circle = np.vstack([p_post1, p_post2[1:]])

    positions = np.vstack([
        p_pre_circle,
        p_circle[1:-1],
        p_post_circle
    ])

    velocities = np.diff(positions, axis=0) / dt
    velocities = np.vstack([velocities, np.zeros(3)])

    X_desired = []

    for i in range(N):
        state = np.hstack([positions[i], velocities[i]])
        X_desired.append(state)

    assert len(X_desired) == N

    return X_desired


# =========================
# LONG TRAJECTORY
# =========================
def desired_trajectory_long(x0, xg, N, dt):

    if N % 2 == 0:

        first_half = desired_trajectory(x0, xg, N//2, dt)

        second_half = [xg.copy() for _ in range(N//2)]

        return first_half + second_half

    else:
        raise ValueError("N must be even")


# =========================
# SKEW MATRIX
# =========================
def skew(v):

    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])


# =========================
# DCM FROM PHI
# =========================
def dcm_from_phi(phi):

    theta = np.linalg.norm(phi)

    if abs(theta) > 1e-12:
        r = phi / theta
    else:
        r = np.zeros(3)

    Q = (
        np.eye(3)
        + np.sin(theta) * skew(r)
        + (1 - np.cos(theta)) * skew(r) @ skew(r)
    )

    return Q


# =========================
# STATE ESTIMATE
# =========================
def state_estimate(xi, xg):

    if np.linalg.norm(xi - xg) < 1:
        return xi

    position_sigma = 0.01
    velocity_sigma = 0.0001

    noise = np.hstack([
        position_sigma * np.random.randn(3),
        velocity_sigma * np.random.randn(3)
    ])

    return xi + noise


# =========================
# THRUSTER MODEL
# =========================
def thruster_model(xi, xg, u):

    if np.linalg.norm(xi - xg) < 1:
        return u

    misalignment = dcm_from_phi(np.deg2rad(3) * np.array([.3, .6, -.8]))

    scale = np.diag([.95, 1.03, 1.01])

    return misalignment @ scale @ u


def animate_rendezvous(X, Xref, dt, show_reference=True):

    vis = mc.Visualizer()
    


    base_path = os.path.dirname(__file__)

    # ---------- DRAGON ----------
    dragon_path = os.path.join(base_path, "dragon.obj")

    vis["dragon"]["base"].set_object(
        geom.ObjMeshGeometry.from_file(dragon_path),
        geom.MeshPhongMaterial(color=0x9999ff)
    )

    vis["dragon"]["base"].set_transform(
        tf.translation_matrix([0,0,-0.34])
        @ tf.rotation_matrix(np.pi/2, [1,0,0])
        @ tf.scale_matrix(0.002)
    )


    # ---------- ISS ----------
    iss_path = os.path.join(base_path, "ISS.obj")

    vis["iss"]["base"].set_object(
        geom.ObjMeshGeometry.from_file(iss_path),
        geom.MeshPhongMaterial(color=0x999999)
    )

    vis["iss"]["base"].set_transform(
        tf.translation_matrix([-8.915,-2.5,4])
        @ tf.rotation_matrix(np.pi/2, [1,0,0])
        @ tf.scale_matrix(0.023)
    )


    # ---------- TRAJECTORY ----------
    if show_reference:
        for i, x in enumerate(Xref):
            vis["traj"][str(i)].set_object(
                geom.Sphere(0.03),
                geom.MeshLambertMaterial(color=0x00ff00)
            )
            vis["traj"][str(i)].set_transform(
                tf.translation_matrix(x[0:3])
            )

    # ---------- ANIMATION ----------
    fps = int(1/dt)
    anim = mc.animation.Animation(default_framerate=fps)

    for k in range(len(X)):
        with anim.at_frame(vis["dragon"], k) as frame:
            x = X[k][0]
            y = X[k][1]
            T = tf.translation_matrix(X[k][0:3])
            R = tf.rotation_matrix(np.pi, [0,0,1])
            frame.set_transform(T @ R)

    vis.set_animation(anim)

    # enable timeline + autoplay
    vis["/"].set_property("animation", {"play": True})

    return vis

