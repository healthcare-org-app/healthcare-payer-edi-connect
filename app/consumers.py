"""Kafka consumers for payer-edi-connect.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("payer-edi-connect.consumers")

TABLE = "payer_edi_connect"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("claim.submitted")
    def _on_claim_submitted(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Simulate EDI 837 handoff. Real impl would push to a payer's SFTP/EDI endpoint.
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"claim_id": data.get("id"), "transport": "EDI-837",
                                      "dispatched_at": envelope.get("occurred_at"),
                                      "status": "queued"}),))
        except Exception as e:
            log.exception("payer-edi-connect/claim.submitted handler failed: %s", e)
        emit_audit(bus, action="consume.claim.submitted", actor="system:payer-edi-connect",
                   target=None, details={"envelope_id": envelope.get("id")})

