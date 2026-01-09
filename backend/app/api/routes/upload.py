from fastapi import APIRouter, UploadFile
from app.services import parser, plots, stats

router = APIRouter()


# route to import .zip and generate stats and plots
@router.post("/upload")
async def upload(file: UploadFile):
    # call imported parser module to unpack zip and store data
    messages = parser.parse(file.file)

    # call imported stats module to calculate stats from extract above
    stats_summary = stats.compute_stats(messages)

    # call imported plots module to generate plots from extract above
    plot_pics = plots.generate_plots(messages)

    # output stats and plots

    return {"stats": stats_summary, "charts": plot_pics}
