# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 18:45
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations


SQL = """
----------------------------------------------------------------------
-- Keeps track of our flowpathcounts as steps are updated
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_update_flowpathcount() RETURNS TRIGGER AS $$
DECLARE flow_id int;
BEGIN

  IF TG_OP = 'TRUNCATE' THEN
    -- FlowStep table being cleared, reset all counts
    DELETE FROM flows_flownodecount;
    DELETE FROM flows_flowpathcount;

  -- FlowStep being deleted
  ELSIF TG_OP = 'DELETE' THEN

    -- ignore if test contact
    IF temba_contact_is_test(OLD.contact_id) THEN
      RETURN NULL;
    END IF;

    flow_id = temba_flow_for_run(OLD.run_id);

    IF OLD.left_on IS NULL THEN
      PERFORM temba_insert_flownodecount(flow_id, UUID(OLD.step_uuid), -1);
    END IF;

    IF OLD.rule_uuid IS NOT NULL AND OLD.next_uuid IS NOT NULL THEN
      PERFORM temba_insert_flowpathcount(flow_id, UUID(OLD.rule_uuid), UUID(OLD.next_uuid), OLD.left_on, -1);
    END IF;

  -- FlowStep being added or left_on field updated
  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN

    -- ignore if test contact
    IF temba_contact_is_test(NEW.contact_id) THEN
      RETURN NULL;
    END IF;

    flow_id = temba_flow_for_run(NEW.run_id);

    IF NEW.left_on IS NULL THEN
      PERFORM temba_insert_flownodecount(flow_id, UUID(NEW.step_uuid), 1);
    END IF;

    IF NEW.rule_uuid IS NOT NULL AND NEW.next_uuid IS NOT NULL THEN
      PERFORM temba_insert_flowpathcount(flow_id, UUID(NEW.rule_uuid), UUID(NEW.next_uuid), NEW.left_on, 1);
    END IF;

    IF TG_OP = 'UPDATE' AND OLD.left_on IS NULL THEN
      PERFORM temba_insert_flownodecount(flow_id, UUID(OLD.step_uuid), -1);
    END IF;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION temba_step_from_uuid(flows_flowstep);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0131_add_flowrun_index'),
    ]

    operations = [
        migrations.RunSQL(SQL),
    ]
