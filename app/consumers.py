"""Kafka consumers for payer-edi-connect.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("payer-edi-connect.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("claim.submitted")
    def _on_claim_submitted(envelope: dict) -> None:
        log.info("payer-edi-connect: received claim.submitted id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.claim.submitted", actor="system:payer-edi-connect",
                   target=None, details={"envelope_id": envelope.get("id")})

