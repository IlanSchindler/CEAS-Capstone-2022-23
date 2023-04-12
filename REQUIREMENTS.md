# Requirements

This document holds the current requirements for FlyMASTER2.

## UAV Manager

- Interface
  - Set takeoff mission.
  - Set landing mission.
  - Set, insert, append user mission items.
  - Set, insert, append swarm mission items.
  - Set vehicle active/inactive.
- Vehicles
  - Interface for controlling vehicles.
  - Subclasses for MultiRotor, FixedWing, and Rovers
  - Further subclassing if needed.
  - Abstract away vehicle interactions.
- Tasks
  - Object structure for mission items (single waypoint, waypoint missions, rtl, etc.)
  - Based off of JSON task settings.
  - Verify settings in constructor.
  - MUST BE INTERRUPTABLE (Watch self._exit_flag (Event))
  - Provide estimate based on vehicle.
- Interrupts
  - Need interrupt function.
  - Handle interrupt function.
  - Passes vehicle for checking and control.

## Swarm Manager

- Interface
  - Push missions to swarm.
  - Distributed consensus algorithm for assignment.
  - Keep track of which mission items are swarm.

## Web GUI

- Map Display
  - Draw all vehicles.
  - Highlight the selected vehicle.
  - Draw updating flight paths.
  - Draw any flight boundaries.
  - Draw any obstacles.
  - Dropdown to change map.
  - Right click to insert waypoints.

- UAV Status Sidebar (Two sidebars)
  - Attitude indicator.
  - Show UAV status.
  - Set UAV status.
  - Show vehicle type.
  - Show telemetry feilds:
    - Altitude AGL and MSL.
    - Heading.
    - Ground speed.
    - Air speed.
    - Climb rate.
  - Show throttle progressbar.
  - Show battery progressbar.
  - View user-assigned missions (Has UID).
  - Add/Remove user-assigned missions.
  - View swarm-assigned missions (Has UID).
  - Set in swarm mode or individual mode.

- Mission and Swarm Sidebar
  - View all available UAV missions.
  - Create/Delete UAV missions.
  - View swarm mission staging.
  - Add/Remove/Push missions in swarm staging.

- Console Output
  - Console output section for FlyMASTER2 logs.
  - Console output section for autopilot logs.

- Mission Creator
  - Generate JSON missions.
  - Pick waypoints from map.
  - Maybe have handlers for planning different tasks?

- Camera Control Sidebar
  - View feed from an attached camera.
  - Control gimbal?
  - Latitude/Longitude tracking?
