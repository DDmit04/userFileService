filename_update_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"]
}

file_comment_update_schema = {
    "type": "object",
    "properties": {
        "comment": {"type": "string"},
    },
    "required": ["comment"]}

filepath_update_schema = {
    "type": "object",
    "properties": {
        "path": {"type": "string"},
    },
    "required": ["path"]}

file_level_search_schema = {
    "type": "object",
    "properties": {
        "level": {"type": "string"},
    },
    "required": ["level"]}

add_file_record_schema = {

}
