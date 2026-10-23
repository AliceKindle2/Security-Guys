"""
SecurityGuys - INTENTIONALLY NON-COMPLIANT data model.

This file is a training artifact. Every violation below is deliberate and
annotated with the GDPR article / CCPA-CPRA right it breaks. Do NOT copy these
patterns into a real system.

Legend
  GDPR = Regulation (EU) 2016/679
  CCPA = California Consumer Privacy Act, as amended by CPRA (Cal. Civ. Code 1798.100 et seq.)
"""
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    # ------------------------------------------------------------------
    # Original columns (kept as-is; compliance notes added)
    # ------------------------------------------------------------------
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # VIOLATION: GDPR Art. 5(1)(f) + Art. 32 (integrity/confidentiality, security of
    # processing) - password stored in plaintext instead of a salted, slow hash.
    # CCPA 1798.150 - exposes the business to statutory damages after a breach of
    # unencrypted/unredacted personal information.
    password: Mapped[str] = mapped_column(String(255))

    # VIOLATION: GDPR Art. 32 + Art. 5(1)(c) - national identifier stored unencrypted
    # and with no demonstrated need. CCPA 1798.140(ae) - SSN is Sensitive Personal
    # Information; 1798.150 breach liability applies to plaintext SSNs.
    ssn: Mapped[str] = mapped_column(String(11))

    date_of_birth: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20))

    # VIOLATION: GDPR Art. 9(1) - health data is special-category data; no explicit
    # consent (Art. 9(2)(a)) or other Art. 9(2) condition recorded, and no encryption
    # (Art. 32). CCPA 1798.140(ae) - health info is Sensitive Personal Information.
    # (HIPAA would also apply to a real patient portal.)
    medical_history: Mapped[str] = mapped_column(Text)

    # ------------------------------------------------------------------
    # Forced opt-in / bundled consent
    # ------------------------------------------------------------------
    # VIOLATION: GDPR Art. 7(4) + Recital 32 (consent must be freely given and
    # unambiguous; pre-ticked boxes are not valid consent) and Art. 25(2) (privacy by
    # default - only necessary data processed unless the user opts in). Marketing is
    # on by default.
    marketing_consent: Mapped[bool] = mapped_column(Boolean, default=True)

    # VIOLATION: CCPA 1798.120 + 1798.135 (Right to Opt-Out of Sale/Sharing; a
    # "Do Not Sell or Share My Personal Information" mechanism is required, and
    # there is none here). GDPR Art. 6(1)(a) + Art. 7 - no lawful basis for
    # disclosing data to third parties; Art. 25(2) - privacy-hostile default.
    allow_third_party_data_sale: Mapped[bool] = mapped_column(Boolean, default=True)

    # VIOLATION: GDPR Art. 7(1) (controller must be able to DEMONSTRATE consent) and
    # Art. 13 (transparency). A bare boolean with no accepted_at timestamp, no
    # policy_version and no IP/user-agent evidence cannot prove who agreed to what.
    # Default=True also means "accepted" without any affirmative act (Art. 4(11)).
    privacy_policy_accepted: Mapped[bool] = mapped_column(Boolean, default=True)

    # ------------------------------------------------------------------
    # Excessive collection / special-category data
    # (defaults are empty strings so the existing /signup route keeps working)
    # ------------------------------------------------------------------
    # VIOLATION: GDPR Art. 5(1)(c) (data minimisation) + Art. 9(1) (biometric data
    # used to uniquely identify a person is special-category). No purpose, no
    # explicit consent. CCPA 1798.100(c) (collection must be reasonably necessary
    # and proportionate) + 1798.121 (limit use of Sensitive PI). Biometrics cannot
    # be rotated once leaked.
    biometric_hash: Mapped[str] = mapped_column(String(255), default="")

    # VIOLATION: GDPR Art. 9(1) (political opinions) + Art. 5(1)(c) - no relevance to
    # a medical portal. CCPA 1798.100(c) (data minimisation) - collection is not
    # reasonably necessary for any disclosed purpose.
    political_affiliation: Mapped[str] = mapped_column(String(255), default="")

    # VIOLATION: GDPR Art. 9(1) (religious or philosophical beliefs) + Art. 5(1)(c).
    # CCPA 1798.140(ae) - religious beliefs are Sensitive Personal Information;
    # 1798.121 gives users the right to limit its use, which is not honoured here.
    religious_beliefs: Mapped[str] = mapped_column(String(255), default="")

    # VIOLATION: GDPR Art. 5(1)(c) + Art. 25(2) (continuous location tracking is not
    # necessary for the stated purpose; not off by default). CCPA 1798.140(ae) -
    # precise geolocation (within ~1,850 ft) is Sensitive Personal Information.
    precise_geolocation: Mapped[str] = mapped_column(String(255), default="")

    # VIOLATION: GDPR Art. 5(1)(c) (a medical portal has no need for card data) and
    # Art. 32 (no encryption/tokenisation). CCPA 1798.140(ae) - account number with
    # access credentials is Sensitive PI; 1798.150 - plaintext card data triggers
    # breach liability. (PCI DSS also forbids storing CVV after authorization and
    # requires PAN to be rendered unreadable.)
    credit_card_number: Mapped[str] = mapped_column(String(255), default="")

    # ------------------------------------------------------------------
    # Anti-erasure / "shadow retention"
    # ------------------------------------------------------------------
    # VIOLATION: GDPR Art. 17(1) (right to erasure) + CCPA 1798.105 (Right to
    # Delete). A soft-delete flag hides the account but the data remains intact
    # and queryable; it is not erasure.
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # VIOLATION: GDPR Art. 5(1)(e) (storage limitation) + Art. 17 + Art. 25(2);
    # CCPA 1798.100(a)(3) (retention period must be disclosed and no longer than
    # reasonably necessary). Default=True means every user is retained indefinitely
    # even after a deletion request.
    retain_forever: Mapped[bool] = mapped_column(Boolean, default=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------
    # VIOLATION: GDPR Art. 17(1) + Art. 17(2) / Art. 19 (erasure must reach all
    # copies and recipients). No cascade="all, delete-orphan" and no
    # passive_deletes: removing a User leaves children behind (SQLAlchemy only
    # nulls the FK) and each child also carries its own PII copy (see below).
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="user")
    prescriptions: Mapped[list["Prescription"]] = relationship(back_populates="user")
    broker_logs: Mapped[list["ThirdPartyDataBrokerLog"]] = relationship(back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    # VIOLATION: GDPR Art. 17(1) - no ondelete="CASCADE" / "SET NULL" policy, so
    # deleting the user does not delete the appointment. Nullable on purpose so the
    # row can be orphaned and still survive.
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # VIOLATION: GDPR Art. 5(1)(c) (data minimisation - the user_id join is enough),
    # Art. 5(1)(d)/(f) (duplicated copies drift out of sync and multiply breach
    # surface), and Art. 17 (erasure of the User row does not reach these copies).
    # CCPA 1798.105 - a Right to Delete request cannot be fully honoured.
    patient_ssn: Mapped[str] = mapped_column(String(11))
    patient_full_name: Mapped[str] = mapped_column(String(100))
    patient_email: Mapped[str] = mapped_column(String(255))

    doctor_name: Mapped[str] = mapped_column(String(100))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)

    # VIOLATION: GDPR Art. 9(1) + Art. 32 - free-text clinical reason stored
    # unencrypted with no access controls.
    reason: Mapped[str] = mapped_column(Text)

    user: Mapped[Optional["User"]] = relationship(back_populates="appointments")


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    # VIOLATION: GDPR Art. 17(1) - missing ondelete="CASCADE"; prescription history
    # outlives the user row.
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # VIOLATION: GDPR Art. 5(1)(c), 5(1)(f), Art. 17, and Art. 9 (a name tied to a
    # medication reveals health data). Same duplicated-PII flaw as Appointment;
    # CCPA 1798.105 (Right to Delete) cannot be satisfied by deleting users alone.
    patient_ssn: Mapped[str] = mapped_column(String(11))
    patient_full_name: Mapped[str] = mapped_column(String(100))
    patient_email: Mapped[str] = mapped_column(String(255))

    # VIOLATION: GDPR Art. 9(1) + Art. 32 - medication data is health data and is
    # stored in plaintext with no field-level protection.
    medication_name: Mapped[str] = mapped_column(String(255))
    dosage: Mapped[str] = mapped_column(String(100))
    prescribing_doctor: Mapped[str] = mapped_column(String(100))
    prescribed_at: Mapped[datetime] = mapped_column(DateTime, default=_now)

    user: Mapped[Optional["User"]] = relationship(back_populates="prescriptions")


# VIOLATION (whole table): CCPA 1798.120 / 1798.135 (Right to Opt-Out of Sale or
# Sharing) and GDPR Art. 6(1)(a), Art. 21 (right to object) and Art. 22 (profiling /
# automated decisions). Patient profiles are sold to ad networks with no opt-out
# check, no lawful basis and no disclosure to the data subject (Art. 13/14).
class ThirdPartyDataBrokerLog(Base):
    __tablename__ = "third_party_data_broker_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    # VIOLATION: GDPR Art. 17(1) / Art. 19 - no cascade, and no mechanism to tell the
    # broker (a recipient) to erase the data (Art. 17(2)).
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    broker_name: Mapped[str] = mapped_column(String(255))

    # VIOLATION: GDPR Art. 5(1)(c) + Art. 9 + Art. 32 - an unfiltered dump of the full
    # profile (health data, SSN, beliefs) is sent to the buyer. CCPA 1798.121 -
    # Sensitive PI disclosed without the user being able to limit it.
    data_payload_dump: Mapped[str] = mapped_column(Text)

    # Records that a sale for monetary value occurred (CCPA 1798.140(ad) "sale").
    sold_price: Mapped[float] = mapped_column(Float)
    shared_at: Mapped[datetime] = mapped_column(DateTime, default=_now)

    # VIOLATION: CCPA 1798.120(c) (businesses must not sell data of consumers under 16
    # without opt-in: the consumer's own at 13-15, a parent or guardian's under 13) and
    # GDPR Art. 8 (child's consent requires parental authorization below the national
    # age threshold, 13-16) + Recital 38/71 (children's data and profiling).
    # The flags exist but are never enforced: minors are sold by default.
    subject_is_minor: Mapped[bool] = mapped_column(Boolean, default=False)
    parental_consent_obtained: Mapped[bool] = mapped_column(Boolean, default=False)

    # VIOLATION: GDPR Art. 7(1) - no record of when/how consent or an opt-out check
    # was verified before the sale; consent cannot be demonstrated.
    consent_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[Optional["User"]] = relationship(back_populates="broker_logs")


# VIOLATION (whole table): GDPR Art. 5(1)(e) (storage limitation) and Art. 5(1)(c)
# (minimisation). Request bodies are logged verbatim and kept forever, so the log
# becomes a second, unprotected copy of every user's PII/PHI.
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    # VIOLATION: GDPR Art. 17(1) - logs are exempt from erasure; no cascade.
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    action: Mapped[str] = mapped_column(String(255))

    # VIOLATION: GDPR Art. 5(1)(c) + Art. 32 - raw request payloads (passwords, SSNs,
    # medical history, card numbers) are written in plaintext. CCPA 1798.150 -
    # breach of this table exposes unencrypted Sensitive PI.
    raw_request_body: Mapped[str] = mapped_column(Text)

    # VIOLATION: GDPR Art. 4(1) / Recital 30 - IP addresses and user agents are
    # personal data (online identifiers); collected without notice or purpose
    # limitation (Art. 5(1)(b), Art. 13).
    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str] = mapped_column(String(512))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)

    # VIOLATION: GDPR Art. 5(1)(e) - there is deliberately NO expires_at / ttl /
    # purge_after column, and no delete path: records are effectively immutable and
    # permanent. CCPA 1798.100(a)(3) - no retention limit that could be disclosed.

    user: Mapped[Optional["User"]] = relationship(back_populates="audit_logs")

