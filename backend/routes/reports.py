from datetime import date

from fastapi import APIRouter, Depends, Response

from backend.core.security import role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.reports import IndicatorsReport
from backend.services.reports import get_indicators_report, indicators_report_to_csv


router = APIRouter(prefix="/relatorios")


@router.get("/indicadores", response_model=IndicatorsReport)
def indicadores(
    created_from: date | None = None,
    created_to: date | None = None,
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    return get_indicators_report(created_from=created_from, created_to=created_to)


@router.get("/indicadores/export.csv")
def export_indicadores_csv(
    created_from: date | None = None,
    created_to: date | None = None,
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    report = get_indicators_report(created_from=created_from, created_to=created_to)
    content = indicators_report_to_csv(report)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="relatorio-indicadores.csv"',
        },
    )
