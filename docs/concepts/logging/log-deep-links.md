# Log deep links

A log deep link connects an application's UI to a query in the central logging system. For example,
a user inspecting a failed operation can open the logs for its trace ID without copying the ID and
constructing a search manually.

[Distributed tracing](distributed-tracing.md) provides the correlation identifier. The application
constructs a link from that identifier; the logging system executes the query and controls access
to its results.

## Constructing a link

1. Obtain the trace ID associated with the operation being displayed.
2. Choose a query URL for the deployment's logging backend, including the appropriate log groups or index.
3. Insert the trace ID into the query, preserving the logging backend's URL encoding.
4. Offer the link next to the operation or its trace ID.

A configurable URL template allows the logging backend to change between environments. The examples
below use `{traceId}` as a placeholder. The application must implement its replacement; the logging
backend does not interpret this placeholder. The property's name and any default template belong
in the documentation of the application or component providing the link.

Access to the application does not itself grant access to the logging system. Users opening a link
need permission to run the target query.

## Query examples

### Splunk

This example searches the `msg.traceId` field over the last month. Adapt the host, field and search
scope to the deployed logging configuration:

```text
https://splunk.example.com/en-GB/app/search?q=search%20msg.traceId%3D{traceId}%20earliest%3D-1mon
```

### AWS CloudWatch

A Logs Insights query can filter by the trace ID, for example:

```text
fields @timestamp, @message, @log
| filter traceId = "{traceId}"
| sort @timestamp desc
| limit 20
```

Select the appropriate region, log groups, trace-ID field and time range in Logs Insights. A query
link contains an encoded representation of those settings. The following URL illustrates a template;
replace the region placeholders and configure the source log groups before using it:

```text
https://<region>.console.aws.amazon.com/cloudwatch/home?region=<region>#logsV2:logs-insights$3FqueryDetail$3D~(end~0~start~-259200~timeType~'RELATIVE~unit~'seconds~editorString~'fields*20*40timestamp*2c*20*40message*2c*20*40log*0a*7c*20filter*20traceId*20*3d*20*22{traceId}*22*0a*7c*20sort*20*40timestamp*20desc*0a*7c*20limit*2020~source~(~'))
```

## Troubleshooting and verification

Test the template with a trace ID from a known log entry in the target environment. Open the generated
link and confirm that it finds that entry, including after deployment behind the application's normal URL.

| Symptom | What to check |
| --- | --- |
| The query opens but returns no results | Compare the trace-ID field and value with a known log entry. Check the time range, region, log groups or index, and allow for log ingestion delay. |
| The query contains a literal placeholder | Check that the application replaces the configured placeholder and has a trace ID for the displayed operation. |
| The logging system rejects or changes the query | Generate a working link in that logging system and compare its encoding with the template. Avoid encoding an already encoded query a second time. |
| The user receives an access error | Check the user's logging-system session and permissions for the selected log groups or index. |

If no trace ID is available, hide or disable the action with an explanation instead of opening an
unfiltered search. Changes to log format or backend query URLs require checking the template again.

## Related

- [Logging](index.md)
- [Application logs](application-logs.md)
- [Distributed tracing](distributed-tracing.md)
