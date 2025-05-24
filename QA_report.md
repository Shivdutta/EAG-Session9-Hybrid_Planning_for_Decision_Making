# Bug Report: Decision Layer and Memory Integration Issues

## Previous Issues
- The decision layer was unable to access outputs from the perception layer or memory, which limited its ability to make informed decisions.
- Outputs from tools were not saved to memory, causing data to be unavailable for future queries or for use by the decision layer.

## Improvements and Updated Workflow
- **Memory Lookup First:**  
  When a query arrives, the system first searches memory for a relevant answer. This avoids redundant processing and improves response speed for repeated or similar queries.
  
- **Perception Layer Processing:**  
  If no relevant memory entry exists, the query is passed to the perception layer. This layer processes the query, potentially using external tools or models to generate an initial response or extract pertinent information.
  
- **Passing Context to Decision Layer:**  
  Both the original query and the perception layer's output are forwarded to the decision layer, ensuring it has complete context including any new insights or data.
  
- **Decision Making:**  
  The decision layer evaluates the combined information (query + perception output) and decides on next steps, which may include synthesizing a final answer, invoking more tools, or requesting further clarification.
  
- **Tool Output Handling and Memory Update:**  
  Any tool outputs generated during the process are now saved to memory, ensuring new information is retained and accessible for both perception and decision layers in future interactions.

