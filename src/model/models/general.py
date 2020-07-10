"""
Author:     David Walshe
Date:       06 July 2020
"""

from sqlalchemy import Column, Integer, String, Float

from src.model.models.model import Model, Base


class Core(Model):

    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Tag = Column(String, unique=True)


class IncomeAndProduction(Core):
    BailCount = Column(Integer, default=28)
    BuildSpeed = Column(Float, default=0.8)
    GemValue = Column(Integer, default=50)
    GoldValue = Column(Integer, default=25)
    GrowthRate = Column(Float, default=2.0)
    OreGrows = Column(String, default="yes")
    OreSpreads = Column(String, default="yes")
    OreTruckRate = Column(Float, default=1.0)
    SeparateAircraft = Column(String, default="no")
    SurvivorRate = Column(Float, default=0.4)


class CombatAndDamage(Core):
    pass
    # TurboBoost = Column(Float, default=1.5)
    # APMineDamage = Column(Integer, default=1000)
    # AVMineDamage = Column(Integer, default=1200)
    # AtomDamage = Column(Integer, default=1000)
    # BallisticScatter = Column(Float, default=1.0)
    # BridgeStrength = Column(Integer, default=1000)
    # C4Delay = Column(Float, default=0.03)
    # Crush = Column(Float, default=1.5)
    # ExpSpread = Column(Float, default=0.3)
    # FireSupress = Column(Integer, default=1)
    # HomingScatter = Column(Float, default=2.0)
    # MaxDamage = Column(Integer, default=1000)
    # MinDamage = Column(Integer, default=1000)
    # OreExplosive = Column(String, default="no")
    # PlayerAutoCrush = Column(String, default="no")
    # PlayerReturnFire = Column(String, default="no")
    # PlayerScatter = Column(String, default="no")
    # ProneDamage = Column(Float, default=0.5)
    # TreeTargeting = Column(String, default="no")
    # Incoming = Column(Integer, default=10)


class Crates(Core):
    pass
    # CrateMinimum = Column(Integer, default=1)
    # CrateMaximum = Column(Integer, default=255)
    # CrateRadius = Column(Float, default=3.0)
    # CrateRegen = Column(Integer, default=3)
    # UnitCrateTye = Column(String, default="none")
    # WaterCrateChance = Column(Float, default=0.2)


class RepairAndRefit(Core):
    pass
    # RefundPercent = Column(Float, default=0.5)
    # ReloadRate = Column(Float, default=0.04)
    # RepairPercent = Column(Float, default=0.20)
    # RepairRate = Column(Float, default=0.016)
    # RepairStep = Column(Integer, default=7)
    # URepairPercent = Column(Float, default=0.2)
    # URepairStep = Column(Integer, default=10)


class SpecialWeapons(Core):
    pass
    # GapRadius = Column(Integer, default=10)
    # GapRegenInterval = Column(Float, default=0.1)
    # IronCurtain = Column(Float, default=0.75)
    # RadarJamRadius = Column(Integer, default=15)


class General(IncomeAndProduction, CombatAndDamage, Crates, RepairAndRefit, SpecialWeapons):

    pass


class GeneralDefaults(General, Base):

    __tablename__ = "general_default"


class GeneralCustom(General, Base):

    __tablename__ = "general_custom"
