"""
Script to fix existing Result records in the database
This updates the incorrect_answers field for all existing results
"""
from app import create_app
from app.extensions.database import db
from app.models.result import Result

def fix_results():
    """Fix all existing result records"""
    app = create_app()
    
    with app.app_context():
        # Get all results
        results = Result.query.all()
        
        print(f"Found {len(results)} results to check...")
        
        fixed_count = 0
        for result in results:
            try:
                # Check if incorrect_answers needs to be calculated
                if result.incorrect_answers is None or result.incorrect_answers == 0:
                    # Calculate incorrect_answers from total and correct
                    if result.total_questions and result.correct_answers is not None:
                        result.incorrect_answers = result.total_questions - result.correct_answers - (result.unanswered or 0)
                        fixed_count += 1
                        print(f"Fixed result ID {result.id}: incorrect_answers = {result.incorrect_answers}")
            except Exception as e:
                print(f"Error fixing result ID {result.id}: {str(e)}")
                continue
        
        # Commit all changes
        if fixed_count > 0:
            db.session.commit()
            print(f"\n✅ Successfully fixed {fixed_count} results!")
        else:
            print("\n✅ All results are already correct!")
        
        return fixed_count

if __name__ == '__main__':
    try:
        fixed = fix_results()
        print(f"\nTotal fixed: {fixed}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
