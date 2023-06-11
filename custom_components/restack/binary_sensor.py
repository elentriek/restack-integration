"""ReStack binary_sensor platform."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyrestack import Stack

from . import ReStackDataUpdateCoordinator
from .const import DOMAIN
from .entity import ReStackEntity
from .utils import format_entity_name


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ReStack binary_sensors."""
    coordinator: ReStackDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ReStackBinarySensor(
            coordinator,
            BinarySensorEntityDescription(
                key=str(stack.name),
                name=stack.name,
                device_class=BinarySensorDeviceClass.CONNECTIVITY,
            ),
            stack=stack,
        )
        for stack in coordinator.data
    )


class ReStackBinarySensor(ReStackEntity, BinarySensorEntity):
    """Representation of a ReStack binary sensor."""

    def __init__(
        self,
        coordinator: ReStackDataUpdateCoordinator,
        description: EntityDescription,
        stack: Stack,
    ) -> None:
        """Set entity ID."""
        super().__init__(coordinator, description, stack)
        self.entity_id = (
            f"binary_sensor.restack_{format_entity_name(self.stack.name)}"
        )

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return self.stack_available
    
    @property
    def extra_state_attributes(self):
        return self.stack_job_attributes