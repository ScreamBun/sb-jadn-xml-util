<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="all"
    expand-text="yes"
    version="3.0">

    <xsl:output method="html" indent="yes" />
    <xsl:mode on-no-match="shallow-copy" />
    <xsl:template  match="/*" mode="#all">
        <div>
            <body>
                <xsl:apply-templates select="*" />
            </body>
        </div>

    </xsl:template>


</xsl:stylesheet>