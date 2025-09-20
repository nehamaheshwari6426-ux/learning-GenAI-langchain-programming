from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

def write_reprot(filename, html):
    with open(filename, 'w') as f:
        f.write(html)
    # return f"Report written to {filename}"

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_reprot,
    args_schema=WriteReportArgsSchema
)