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
        # self._attr_extra_state_attributes = {
        #     "monitor_cert_days_remaining": self.monitor.monitor_cert_days_remaining,
        #     "monitor_cert_is_valid": self.monitor.monitor_cert_is_valid,
        #     "monitor_hostname": self.monitor.monitor_hostname,
        #     "monitor_name": self.monitor.monitor_name,
        #     "monitor_port": self.monitor.monitor_port,
        #     "monitor_response_time": self.monitor.monitor_response_time,
        #     "monitor_status": self.monitor.monitor_status,
        #     "monitor_type": self.monitor.monitor_type,
        #     "monitor_url": self.monitor.monitor_url,
        # }
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
        if self.stack.jobs is not None:
            return bool(self.stack.jobs[0].success)
        else:
            return False