import itertools
import random
from typing import List
from dataclasses import dataclass

from aido_schemas import Context, FriendlyPose
from dt_protocols import (
    Circle,
    CollisionCheckQuery,
    CollisionCheckResult,
    MapDefinition,
    PlacedPrimitive,
    Rectangle,
)

__all__ = ["CollisionChecker"]


class CollisionChecker:
    params: MapDefinition

    def init(self, context: Context):
        context.info("init()")

    def on_received_set_params(self, context: Context, data: MapDefinition):
        context.info("initialized")
        self.params = data

    def on_received_query(self, context: Context, data: CollisionCheckQuery):
        collided = check_collision(
            environment=self.params.environment, robot_body=self.params.body, robot_pose=data.pose
        )
        result = CollisionCheckResult(collided)
        context.write("response", result)

@dataclass 
class PlacedPrimitiveMatrix:
    primitive: PlacedPrimitive
    transform: np.array


def check_collision(
    environment: List[PlacedPrimitive], robot_body: List[PlacedPrimitive], robot_pose: FriendlyPose
) -> bool:
    # This is just some code to get you started, but you don't have to follow it exactly

    # TODO you can start by rototranslating the robot_body by the robot_pose
    robot_p_angle = np.deg2rad(robot_pose.theta_deg)
    robot_p_m = np.array([
        [np.cos(robot_p_angle), -np.sin(robot_p_angle), robot_pos.x],
        [np.sin(robot_p_angle), np.cos(robot_p_angle), robot_pos.y],
        [0, 0, 1],
    ])

    rototranslated_robot: List[PlacedPrimitiveMatrix] = []

    for rb in robot_body:
        rb_a = np.deg2rad(rb.pose.theta_deg)
        
        rb_m = np.array([
            [np.cos(rb_a), -np.sin(rb_a), rb.pose.x],
            [np.sin(rb_a), np.cos(rb_a), rb.pose.y],
            [0, 0, 1],
        ])

        rb_w = np.matmul(robot_p_m, rb_m)
        rototranslated_robot.append(PlacedPrimitiveMatrix(primitive=rb.primitive, transform=rb_w))

    environment_matrices = []
    for e in environment:
        e_angle = np.deg2rad(e.pose.theta_deg)
        e_m = np.array([
            [np.cos(e_angle), -np.sin(e_angle), e.pose.x],
            [np.sin(e_angle), np.cos(e_angle), e.pose.y],
            [0, 0, 1],
        ])
        environment_matrices.append(PlacedPrimitiveMatrix(primitive=e, transform=e_m))

    # Then, call check_collision_list to see if the robot collides with the environment
    collided = check_collision_list(rototranslated_robot, environment_matrices)

    # TODO return the status of the collision
    # for now let's return a random guess
    return random.uniform(0, 1) > 0.5


def check_collision_list(
    rototranslated_robot: List[PlacedPrimitiveMatrix], environment: List[PlacedPrimitiveMatrix]
) -> bool:
    # This is just some code to get you started, but you don't have to follow it exactly
    for robot, envObject in itertools.product(rototranslated_robot, environment):
        if check_collision_shape(robot, envObject):
            return True

    return False

def check_circle(a: PlacedPrimitiveMatrix, b: PlacedPrimitiveMatrix) -> bool:
    pos_a = np.array([a.transform[0,2], a.transform[1,2]])
    pos_b = np.array([b.transform[0,2], b.transform[1,2]])

    dist = np.linalg.norm(pos_a - pos_b)
    return dist < (a.primitive.radius + b.primitive.radius)

def check_rectangle_circle(a: PlacedPrimitiveMatrix, b: PlacedPrimitiveMatrix):
    # transform the rectangle 
    return true



def check_collision_shape(a: PlacedPrimitiveMatrix, b: PlacedPrimitiveMatrix) -> bool:
    # This is just some code to get you started, but you don't have to follow it exactly

    # TODO check if the two primitives are colliding
    if isinstance(a.primitive, Circle) and isinstance(b.primitive, Circle):
        return check_circle(a, b)
    if isinstance(a.primitive, Rectangle) and isinstance(b.primitive, Circle):
        ...
    if isinstance(a.primitive, Rectangle) and isinstance(b.primitive, Rectangle):
        ...
    ...

    # TODO return the status of the collision
    # for now let's return a random guess
    return random.uniform(0, 1) > 0.5
