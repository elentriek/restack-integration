"""Base ReStack entity."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pyrestack import Stack

from . import ReStackDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN


class ReStackEntity(CoordinatorEntity[ReStackDataUpdateCoordinator]):
    """Base ReStack entity."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: ReStackDataUpdateCoordinator,
        description: EntityDescription,
        stack: Stack,
    ) -> None:
        """Initialize UptimeRobot entities."""
        super().__init__(coordinator)
        self.entity_description = description
        self._stack = stack
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.stack.name))},
            name=self.stack.name,
            manufacturer="ReStack Integration",
            entry_type=DeviceEntryType.SERVICE,
            model=self.stack.type,
        )
        self._attr_extra_state_attributes = {
            "job_started": self.stack.jobs[0].started if isinstance(self.stack.jobs, list) and len(self.stack.jobs) >= 1 else '',
            "job_ended": self.stack.jobs[0].ended if isinstance(self.stack.jobs, list) and len(self.stack.jobs) >= 1 else '',
        }
        self._attr_unique_id = f"restack_{self.stack.name}"
        self.api = coordinator.api

    @property
    def _stacks(self) -> list[Stack]:
        """Return all stacks."""
        return self.coordinator.data or []

    @property
    def stack(self) -> Stack:
        """Return the stack for this entity."""
        return next(
            (
                stack
                for stack in self._stacks
                if str(stack.name) == self.entity_description.key
            ),
            self._stack,
        )

    @property
    def stack_available(self) -> bool:
        """Returtn if the stack is available."""
        if self.stack.jobs is not None and isinstance(self.stack.jobs, list):
            return bool(self.stack.jobs[0].success)
        else:
            return False
        
    @property
    def stack_job_attributes(self):
        return self._attr_extra_state_attributes