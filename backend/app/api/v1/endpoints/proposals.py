"""
Proposals API endpoints (Admin only - Internal system)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.services.proposal_service import ProposalService
from app.schemas.proposal import ProposalCreate, ProposalResponse, ProposalListItem

router = APIRouter()


@router.post("/", response_model=ProposalResponse, status_code=201)
def create_proposal(
    proposal_data: ProposalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new proposal from an existing event
    Generates snapshot of all event data at this moment
    """
    try:
        proposal = ProposalService.create_from_event(
            db=db,
            event_id=proposal_data.event_id,
            title=proposal_data.title,
            description=proposal_data.description,
            valid_days=proposal_data.valid_days,
            discount_amount=proposal_data.discount_amount,
            notes=proposal_data.notes
        )
        return proposal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
def list_proposals(
    skip: int = 0,
    limit: int = 10,
    event_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    List all proposals with pagination
    Optionally filter by event_id
    """
    result = ProposalService.list_proposals(db, skip, limit, event_id)
    
    # Enrich list items with data from snapshots
    enriched_items = []
    for proposal in result["items"]:
        item_dict = {
            "id": proposal.id,
            "event_id": proposal.event_id,
            "version_number": proposal.version_number,
            "title": proposal.title,
            "total_amount": proposal.total_amount,
            "valid_until": proposal.valid_until,
            "is_accepted": bool(proposal.is_accepted),
            "generated_at": proposal.generated_at,
            # Extract from snapshots
            "client_name": proposal.client_snapshot.get("name") if proposal.client_snapshot else None,
            "event_name": proposal.event_snapshot.get("name") if proposal.event_snapshot else None,
            "event_date": proposal.event_snapshot.get("date") if proposal.event_snapshot else None,
        }
        enriched_items.append(item_dict)
    
    return {
        "items": enriched_items,
        "total": result["total"],
        "page": result["page"],
        "size": result["size"]
    }


@router.get("/{proposal_id}", response_model=ProposalResponse)
def get_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific proposal by ID
    """
    proposal = ProposalService.get_proposal(db, proposal_id)
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return proposal


@router.delete("/{proposal_id}", status_code=204)
def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a proposal
    """
    success = ProposalService.delete_proposal(db, proposal_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return None
