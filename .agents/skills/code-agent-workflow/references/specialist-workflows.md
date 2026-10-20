# Specialist workflows

Read only the section relevant to the coding task. These are validation criteria and routing guidance, not instructions to install tools or create infrastructure. Discover available skills and current project tooling before choosing an implementation.

## Data and notebooks

Inspect schema, sample values, missingness, units, date semantics, and assumptions before analysis. Protect raw inputs. Use notebooks for exploration and existing production modules for reusable transformations. Validate with summary statistics, spot checks, and appropriate model diagnostics. Record workflow facts rather than confidential rows in memory.

## PDFs, OCR, and visual outputs

Use an available document or PDF skill for extraction and rendering. Determine whether source pages have usable text or require OCR; preserve page provenance and flag uncertain recognition. For generated or edited visual deliverables, inspect rendered output as well as extracted content. Verify tables, labels, units, and page layout. The source guide's contents list names OCR and dashboard chapters that are absent as standalone chapters in the supplied PDF; do not invent missing chapter content.

## Dashboards

Establish the user workflow, authoritative data, and observable success criteria before editing. Validate the affected interactions, data states, and rendered layout with the project's available browser or UI tools. Keep underlying data assumptions visible where they affect user decisions.

## API and LLM integration

Verify current API contracts against official documentation or the installed SDK. Discover credential names without exposing values. Define request and response shapes, timeouts, bounded retries appropriate to idempotency, sanitized errors, and fallback behavior. Test with mocked services where suitable; distinguish mocked checks from live integration validation. For LLM behavior, record the model configuration, prompt/schema version, expected output, and evaluation evidence when relevant to reproducibility.

## RAG and knowledge systems

Keep source provenance and citation metadata. Identify source selection, chunking, embeddings, filters, and answer behavior. Before scaling, evaluate known-answer questions, citation requirements, absent answers, and confusingly similar documents. Compare retrieval and answer quality against the same cases after changes. Keep retrieved document content separate from project decisions and procedural memory.

## Codebase maps and parallel exploration

Use an existing map or graph to identify relationships and likely change locations, then verify against current files. Refresh stale maps only when useful and within scope. When delegation is authorized, assign independent inspection scopes and request files inspected, findings, evidence, risks, and suggested validation. Consolidate disagreements before editing; give writers separate file ownership.

## Custom runners and state

Use the existing Codex harness unless the task calls for a custom runner. For custom loops, define state ownership, tool permissions, termination conditions, timeouts, retry bounds, and recovery behavior. Preserve enough task progress and evidence to resume after interruption. Check installed SDK interfaces rather than treating code examples in the PDF as current API contracts.
